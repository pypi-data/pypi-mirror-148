from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils.module_loading import import_string
from django.views.generic.base import TemplateView

from fints.client import FinTS3PinTanClient, NeedRetryResponse, NeedTANResponse

from .forms import AccountForm, BankCredentialsForm, TANForm, TANMechanismForm, TANMediumForm
from ..models import SEPAMandate


class FinTSView(TemplateView):
    """State-driven handler view for a FinTS SEPA transaction.

    This view handles a complete dialog with a bank to transfer a SEPA
    message, backed by a state machine in the session.

    The view redirects back and forth between asking the user for input
    through various forms and doing FinTS requests according to the input
    and the state.

      GET → _get_current_form() → Is input required?
                                ✓→ Render form → POST
                                ✗→ _do_step() → Step taken? ✓→ GET
                                                            ✗→ success_url
      POST → Handle form → GET
    """

    _SESSION_PREFIX = "fints_view"
    template_name = "djp_sepa/fints/conversation.html"

    @classmethod
    def _set_sepa_message(cls, request, message):
        """Set the SEPA message to be transferred in the session.

        This also invalidates all other state to not confuse any
        on-going dialog.
        """
        if not hasattr(self.request, "session"):
            raise ImproperlyConfigured("The session middleware is needed.")

    @classmethod
    def start_sepadd(cls, request, qs, success_url, success_cb=""):
        """Start a conversation to do SEPA direct debit.

        This method sets the message in the session and returns a redirect
        to the handling view.
        """
        cls._clear_session(request)

        request.session[f"{self._SESSION_PREFIX}_action"] = "sepadd"
        request.session[f"{self._SESSION_PREFIX}_control_sum"] = qs.aggregate(
            control_sum=Sum("payment__total")
        )["control_sum"]
        request.session[f"{self._SESSION_PREFIX}_multiple"] = qs.count() > 1
        request.session[f"{self._SESSION_PREFIX}_currency"] = qs.first().payment.currency
        request.session[f"{self._SESSION_PREFIX}_message"] = (
            SEPAMandate.as_sepadd(qs=qs).export().decode()
        )
        request.session[f"{self._SESSION_PREFIX}_data_pks"] = data.values_list("pk", flat=True)
        request.session[f"{self._SESSION_PREFIX}_success_url"] = success_url
        request.session[f"{self._SESSION_PREFIX}_success_cb"] = success_cb

        cls._set_sepa_message(request, message)

        return redirect("fints_conversation")

    def _get_from_session(self, *args):
        """Get prefixed values from session."""
        if not hasattr(self.request, "session"):
            raise ImproperlyConfigured("The session middleware is needed.")

        ret = []
        for name in args:
            ret.append(self.request.session.get(f"{self._SESSION_PREFIX}_{name}", None))

        if len(ret) == 1:
            return ret[0]
        else:
            return ret

    def _set_in_session(self, **kwargs):
        """Set prefixed values in session."""
        if not hasattr(self.request, "session"):
            raise ImproperlyConfigured("The session middleware is needed.")

        for name, value in kwargs.items():
            self.request.session[f"{self._SESSION_PREFIX}_{name}"] = value

    @classmethod
    def clear_session(cls, request):
        """Clear all prefixed values from the session."""
        if not hasattr(request, "session"):
            raise ImproperlyConfigured("The session middleware is needed.")

        for name in request.session.keys():
            if name.startswith(cls._SESSION_PREFIX):
                del request.session[name]

    def _construct_fints_client(self):
        """Construct a FinTS PIN/TAN client from the session.

        This method looks at the available values in the session, including
        form data and previously serialised client and dialog datan, and
        either creates a completely new FinTS client object or restores it
        into the previous state.
        """
        # First, check whether we have known bank data
        bank_id, login_name, pin, hbci_url = self._get_from_session(
            "bank_id", "login_name", "pin", "hbci_url"
        )
        if None in (bank_id, login_name, pin, hbci_url):
            # If not, we do not know enough yet to create any object
            return None

        # Construct new client object to start with
        client = FinTS3PinTanClient(
            bank_id, login_name, pin, hbci_url, getattr(settings, "FINTS_PRODUCT_ID", None)
        )

        # Check for previously serialised client object and restore if any
        client_data = self._get_from_session("client_data")
        if client_data:
            client.set_data(client_data)

        # Check if TAN mechanism/medium was freshly set
        # This must be set before starting/resuming the dialog
        mechanism, medium = self._get_from_session("tan_mechanism", "tan_medium")
        if mechanism:
            client.set_tan_mechanism(mechanism)
        if medium:
            media = client.get_tan_media()
            client.set_tan_medium(media[1][int(medium)])

        # Store initial TAN response in session, if any
        if client.init_tan_response:
            self._set_in_session("tan_response", client.init_tan_response.get_data())

        return client

    def _deconstruct_fints_client(self):
        """Serialise current client into session."""
        client_data = self._fints_client.deconstruct(including_private=True)
        self._set_in_session(client_data=client_data)

    def _dialog(self, pause=False):
        """Return a context manager with the client's dialog."""
        # Resume any previously serialised dialog
        dialog = self._get_from_session("dialog")
        if dialog:
            self._fints_client = self._fints_client.resume_dialog(dialog)

        with self._fints_client as c:
            yield c

            if pause:
                # Freeze dialog for resumption on next request
                new_dialog = self._fints_client.pause_dialog()
            elif dialog:
                # Clear any previously serialised dialog
                new_dialog = None
            self._set_in_session(dialog=new_dialog)

    def setup(self, request, *args, **kwargs):
        """Setup view with constructed FinTS client."""
        super().setup(request, *args, **kwargs)

        self._fints_client = self._construct_fints_client()

    def dispatch(self, request, *args, **kwargs):
        """Handle request.

        After finishing the request, deconstruct the client, serialising
        its state into the session.
        """
        ret = super().dispatch(request, *args, **kwargs)

        if self._fints_client:
            self._deconstruct_fints_client()

        return ret

    def _get_current_form(self):
        """Get the form for the current state of the conversation."""
        if not self._fints_client:
            # Ask for FinTS login data
            form = BankCredentialsForm(self.request.POST or None)
        elif (
            self.request.GET.get("change_mechanism", False)
            or not self._fints_client.get_current_tan_mechanism()
        ):
            # TAN mechanism not set; ask for supported mechanisms
            mechanisms = self._fints_client.get_tan_mechanisms()
            form = TANMechanismForm(mechanisms, self.request.POST or None)
        elif (
            self.request.GET.get("change_medium", False)
            or not self._fints_client.is_tan_media_required()
            and not self._fints_client.selected_tan_medium
        ):
            # TAN mechanism needs medium, but none is set
            media = self._fints_client.get_tan_media()
            form = TANMediumForm(media, self.request.POST or None)
        elif self._get_from_session("tan_response"):
            tan_response = NeedRetryResponse.from_data(self._get_from_session("tan_response"))
            form = TANForm(tan_response, self.request.POST or None)
        elif not self._get_from_session("account"):
            accounts = self._fints_client.get_sepa_accounts()
            form = AccountForm(accounts, self.request.POST or None)
        else:
            form = None

        return form

    def _handle_response(self, res):
        """Handle a response from FinTS."""
        if isinstance(res, NeedTANResponse):
            # A TAN is required; mark in session to ask on next step
            self._set_in_session("tan_response", res.get_data())

        return res

    def _do_step(self):
        """Do the real step in the FinTS conversation."""
        if self._get_from_session("tan_response"):
            # If we are responding to a TAN challenge, do it here
            with self._dialog():
                # Clear old response from session
                self._set_in_session("tan_response", None)

                # Send TAN from form
                res = self._fints_client.send_tan(
                    self._get_from_session("tan_response"), form.cleaned_data["tan"]
                )
        elif self._get_from_session("action") == "sepadd":
            # Clear action from session to never repeat first step
            self._set_in_session("action", None)

            accounts = self._fints_client.get_accounts()
            account, message, multiple, control_sum, currency = self._get_from_session(
                "account", "message", "multiple", "control_sum", "currency"
            )
            with self._dialog(pause=True):
                res = self._fints_client.sepa_debit(
                    account=accounts[int(account)],
                    pain_message=message,
                    multiple=multiple,
                    control_sum=control_sum if multiple else None,
                    currency=currency,
                    book_as_single=True,
                )
        else:
            res = None

        if res:
            self._handle_response(res)

        return res

    def get(self, request, *args, **kwargs):
        # Check if we already need user input
        if self._get_current_form():
            # If yes, let the default GET view take over
            return super().get(request, *args, **kwargs)
        else:
            # Try to do one step
            res = self._do_step()

        if res:
            # If a step was done, redirect again to try next step
            return redirect("fints_conversation")

        # If we got here, the conversation is over
        success_url, success_cb, data_pks = self._get_from_session(
            "success_url", "success_cb", "data_pks"
        )
        self._clear_session(request)
        if success_cb:
            success_cb = import_string(success_cb)
            success_cb(*(data_pks or []))
        return redirect(success_url)

    def post(self, request, *args, **kwargs):
        """Handle a submitted form to drive the FinTS conversation forward."""
        form = self._get_current_form()
        if form and form.is_valid():
            self._set_in_session(**form.get_session_data())

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get a form and context matching the current conversation state."""
        context = super().get_context_data(**kwargs)
        context["form"] = self._get_current_form()
        return context
