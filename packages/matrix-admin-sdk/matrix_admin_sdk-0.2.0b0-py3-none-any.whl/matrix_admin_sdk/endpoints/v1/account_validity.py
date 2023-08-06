from matrix_admin_sdk.endpoints import RequestMethods
from matrix_admin_sdk.models.v1.account_validity import RenewAccountModel

from .endpoint import Endpoint


class AccountValidity(Endpoint):
    """
    This API allows a server administrator to manage the validity of an account.
    To use it, you must enable the account validity feature (under account_validity)
    in Synapse's configuration.
    """

    async def renew_account(
        self, user_id: str, expiration_ts: int = 0, enable_renewal_emails: bool = True
    ) -> RenewAccountModel:
        """
        This API extends the validity of an account by as much time as configured
        in the period parameter from the account_validity configuration.
        Args:
            user_id: user ID for the account to renew
            expiration_ts: overrides the expiration date, which otherwise defaults
                to now + validity period.
            enable_renewal_emails: enables/disables sending renewal emails to the user.

        Returns: RenewAccountModel
        """
        url = self.url("account_validity/validity")
        data = {
            "user_id": user_id,
            "expiration_ts": expiration_ts,
            "enable_renewal_emails": enable_renewal_emails,
        }
        response = await self.request(RequestMethods.POST, url, json=data)
        res: RenewAccountModel = RenewAccountModel.from_dict(response)
        return res
