"""VoIP.ms IVR (interactive voice response) management."""

from .voipms_client import VoipMsClient
from typing import Optional, Union


class IVR(VoipMsClient):
    """
    IVR operations for the VoIP.ms API.

    Methods:
        create_ivr(name, recording, ...): Create an IVR.
        delete_ivr(ivr): Delete an IVR by ID.
        get_ivrs(ivr): List IVRs or get one by ID.
        update_ivr(id, ...): Update an existing IVR.
    """

    def create_ivr(
        self,
        name: str,
        recording: Union[str, int],
        time_out: Optional[Union[str, int]] = None,
        language: Optional[str] = None,
        voicemail: Optional[str] = None,
        options: Optional[str] = None,
    ) -> dict:
        """
        Create a new IVR (VoIP.ms setIVR).

        Args:
            name: Display name for the IVR.
            recording: Recording ID for the IVR. See get_recordings.
            time_out: Max seconds to dial an option after recording (1–10). Default 5.
            language: Language code (e.g. 'en'). See get_languages. Default 'en'.
            voicemail: '1' = default DID voicemail, '2' = account voicemail. Default '1'.
            options: Semicolon-separated choices (e.g. '1=account:100001;2=fwd:16006'). Default is main account for 1.

        Returns:
            API response with the created IVR data.
        """
        
        mtd = "setIVR"
        params = {
            # Required by this package
            "name": name,
            "recording": recording,

            # Required by VoIP.ms API but set with default values so it is not required in this package.
            "timeout": 5,
            "language": "en",
            "voicemailsetup": 1,
            # The Main Account is the default for option 1; it is only looked up when no options are provided.
            "choices": options or f"1=account:{self._main_account()}"
        }

        # Optional in this package.
        if time_out:
            params["timeout"] = time_out
        if language:
            params["language"] = language
        if voicemail:
            params["voicemailsetup"] = voicemail
        if options:
            params["choices"] = options

        data = self.get(mtd, params)
        data["name"] = name
        return data

    def delete_ivr(self, ivr: Union[str, int]) -> dict:
        """
        Delete an IVR by ID (VoIP.ms delIVR).

        Args:
            ivr: IVR ID to delete (e.g. 18635). Use get_ivrs to list IDs.

        Returns:
            API response with result and IVR name.
        """
        
        mtd = "delIVR"

        params = {
            "ivr": ivr,
        }

        # Code to get the name of the IVR that is deleted.
        ivr_info = self.get_ivrs(ivr)
        ivr_name = self._first(ivr_info, "ivrs", "IVR")["name"]

        data = self.get(mtd, params)
        data["ivr"] = ivr_name
        return data

    def get_ivrs(self, ivr: Optional[Union[str, int]] = None) -> dict:
        """
        List IVRs or get one by ID (VoIP.ms getIVRs).

        Args:
            ivr: Optional IVR ID (e.g. 323). If omitted, all IVRs are returned.

        Returns:
            API response with all IVRs or the requested one.
        """
        
        mtd = "getIVRs"

        params = {}

        # Optional in this package.
        if ivr:
            params["ivr"] = ivr

        data = self.get(mtd, params)
        return data

    def update_ivr(
        self,
        id: Union[str, int],
        name: Optional[str] = None,
        recording: Optional[Union[str, int]] = None,
        time_out: Optional[Union[str, int]] = None,
        language: Optional[str] = None,
        voicemail: Optional[str] = None,
        options: Optional[str] = None,
    ) -> dict:
        """
        Update an existing IVR (VoIP.ms setIVR).

        Args:
            id: IVR ID to update. Use get_ivrs to list IDs.
            name: Display name for the IVR.
            recording: Recording ID. See get_recordings.
            time_out: Max seconds to dial an option (1–10).
            language: Language code. See get_languages.
            voicemail: '1' = default DID voicemail, '2' = account voicemail.
            options: Semicolon-separated choices (e.g. '1=account:100001;2=fwd:16006').

        Returns:
            API response with updated IVR data.
        """
        
        mtd = "setIVR"


        # Code to get the settings of the IVR that will be edited.
        ivr_config = self.get_ivrs(id)
        # Saving the current settings in the parameters.
        params = self._first(ivr_config, "ivrs", "IVR")

        # Optional in this package.
        if recording:
            params["recording"] = recording
        if time_out:
            params["timeout"] = time_out
        if language:
            params["language"] = language
        if voicemail:
            params["voicemailsetup"] = voicemail
        if options:
            params["choices"] = options

        data = self.get(mtd, params)
        data["name"] = name
        return data
