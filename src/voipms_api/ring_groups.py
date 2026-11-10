"""VoIP.ms ring groups management."""

from .voipms_client import VoipMsClient
from typing import Optional, Union


class RingGroups(VoipMsClient):
    """
    Ring group operations for the VoIP.ms API.

    Methods:
        create_ring_group(name, voicemail, ...): Create a ring group.
        delete_ring_group(ring_group): Delete a ring group by ID.
        get_ring_groups(ring_group): List ring groups or get one by ID.
        update_ring_group(id, ...): Update an existing ring group.
    """

    def create_ring_group(
        self,
        name: str,
        voicemail: Union[str, int],
        members: Optional[str] = None,
        announcement: Optional[str] = None,
        music_on_hold: Optional[str] = None,
        language: Optional[str] = None,
    ) -> dict:
        """
        Create a new ring group (VoIP.ms setRingGroup).

        Args:
            name: Display name for the ring group.
            voicemail: Voicemail ID to assign. See get_voicemails.
            members: Semicolon-separated members (e.g. 'account:100001;fwd:16006'). Default is main account only.
            announcement: Caller announcement.
            music_on_hold: Music on hold. See get_music_on_hold.
            language: Language code. See get_languages.

        Returns:
            API response with the created ring group data.
        """
        
        mtd = "setRingGroup"

        params = {
            # Required by this package
            "name": name,
            "voicemail": voicemail,

            # Required by VoIP.ms API but set with a default value so it is not required.
            # The Main Account is the default member; it is only looked up when no members are provided.
            "members": members or f"account:{self._main_account()}",
        }

        # Optional in this package.
        if members:
            params["members"] = members
        if announcement:
            params["caller_announcement"] = announcement
        if music_on_hold:
            params["music_on_hold"] = music_on_hold
        if language:
            params["language"] = language

        data = self.get(mtd, params)
        data["name"] = name
        return data

    def delete_ring_group(self, ring_group: Union[str, int]) -> dict:
        """
        Delete a ring group by ID (VoIP.ms delRingGroup).

        Args:
            ring_group: Ring group ID to delete (e.g. 18635). Use get_ring_groups to list IDs.

        Returns:
            API response with result and ring group name.
        """
        
        mtd = "delRingGroup"

        params = {
            "ringgroup": ring_group,
        }

        # Code to get the name of the ring group that is deleted.
        rg_info = self.get_ring_groups(ring_group)
        rg_name = self._first(rg_info, "ring_groups", "Ring group")["name"]

        data = self.get(mtd, params)
        data["ring_group"] = rg_name
        return data

    def get_ring_groups(self, ring_group: Optional[Union[str, int]] = None) -> dict:
        """
        List ring groups or get one by ID (VoIP.ms getRingGroups).

        Args:
            ring_group: Optional ring group ID (e.g. 18635). If omitted, all are returned.

        Returns:
            API response with all ring groups or the requested one.
        """
        
        mtd = "getRingGroups"

        params = {}

        # Optional in this package.
        if ring_group:
            params["ring_group"] = ring_group

        data = self.get(mtd, params)
        return data

    def update_ring_group(
        self,
        id: Union[str, int],
        name: Optional[str] = None,
        voicemail: Optional[Union[str, int]] = None,
        members: Optional[str] = None,
        announcement: Optional[str] = None,
        music_on_hold: Optional[str] = None,
        language: Optional[str] = None,
    ) -> dict:
        """
        Update an existing ring group (VoIP.ms setRingGroup).

        Args:
            id: Ring group ID to update. Use get_ring_groups to list IDs.
            name: Display name for the ring group.
            voicemail: Voicemail ID. See get_voicemails.
            members: Semicolon-separated members (e.g. 'account:100001;fwd:16006').
            announcement: Caller announcement.
            music_on_hold: Music on hold. See get_music_on_hold.
            language: Language code. See get_languages.

        Returns:
            API response with updated ring group data.
        """
        
        mtd = "setRingGroup"

        # Code to get the settings of the ring group that will be updated.
        rg_config = self.get_ring_groups(id)
        # Saving the current settings in the parameters.
        params = self._first(rg_config, "ring_groups", "Ring group")

        # Optional in this package.
        if name:
            params["name"] = name
        if voicemail:
            params["voicemail"] = voicemail
        if members:
            params["members"] = members
        if announcement:
            params["caller_announcement"] = announcement
        if music_on_hold:
            params["music_on_hold"] = music_on_hold
        if language:
            params["language"] = language

        data = self.get(mtd, params)
        data["name"] = name
        return data
