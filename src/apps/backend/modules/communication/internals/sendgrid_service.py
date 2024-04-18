from modules.communication.errors import ServiceError
from modules.communication.internals.sendgrid_email_params import EmailParams
from modules.communication.types import SendEmailParams
import sendgrid
from sendgrid.helpers.mail import Mail, To, From, TemplateId

from modules.config.config_service import ConfigService

class SendGridService:
    __client: sendgrid.SendGridAPIClient = None

    @staticmethod
    def send_email(params: SendEmailParams) -> None:
        EmailParams.validate(params)

        message = Mail(
            from_email=From(params.sender.email, params.sender.name),
            to_emails=To(params.recipient.email),
        )
        message.template_id = TemplateId(params.template_id)
        message.dynamic_template_data = params.template_data

        try:
            client = SendGridService.get_client()
            client.send(message)  
            
        except sendgrid.exceptions.SendGridException as err:
            raise ServiceError(err)

    @staticmethod
    def get_client() -> sendgrid.SendGridAPIClient:
        if not SendGridService.__client:
            api_key = ConfigService.get_sendgrid_api_key()
            SendGridService.__client = sendgrid.SendGridAPIClient(api_key=api_key)
        return SendGridService.__client
