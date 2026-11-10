"""VoIP.ms DIDs (phone numbers) management."""

from .voipms_client import VoipMsClient
from typing import Optional, Union


class DIDs(VoipMsClient):
    """
    DID (phone number) operations for the VoIP.ms API.

    Methods:
        cancel_did(did, ...): Cancel a DID and optionally add comment/port-out flag.
        get_dids_info(client, did): List DIDs for account, client, or a specific DID.
        order_did(did, ...): Order a local US/Canadian DID.
        order_toll_free(did, ...): Order a toll-free US/Canadian DID.
        set_did_routing(did, routing): Set the routing for a DID.
    """

    def cancel_did(
        self,
        did: Union[str, int],
        comment: Optional[str] = None,
        port_out: Optional[Union[str, bool]] = None,
        test: Optional[Union[str, bool]] = None,
    ) -> dict:
        """
        Cancel a DID (VoIP.ms cancelDID).

        Args:
            did: DID number to cancel (e.g. 5551234567).
            comment: Optional comment for the cancellation.
            port_out: Set True if the DID was ported out.
            test: Set True to test the cancel flow without actually canceling.

        Returns:
            API response with result and the canceled DID.
        """
        
        mtd = "cancelDID"

        params = {
            "did": did,
        }

        if comment:
            params["comment"] = comment
        if port_out:
            params["portout"] = port_out
        if test:
            params["test"] = test

        data = self.get(mtd, params)
        data["result"] = "DID canceled"
        data["did"] = did
        return data

    def get_dids_info(
        self,
        client: Optional[Union[str, int]] = None,
        did: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        Get DID(s) info (VoIP.ms getDIDsInfo).

        Args:
            client: Optional reseller client ID or sub-account (e.g. 123456 or '100000_Account').
            did: Optional specific DID or sub-account to filter by (e.g. 5551234567).

        Returns:
            API response: all DIDs (no args), client's DIDs (client), sub-account DID (did=subaccount), or specific DID (did=number).
        """
        
        mtd = "getDIDsInfo"

        params = {}

        if client:
            params["client"] = client
        if did:
            params["did"] = did

        data = self.get(mtd, params)
        return data

    def order_did(
        self,
        did: Union[str, int],
        routing: Optional[str] = "sys:hangup",
        pop: Optional[Union[str, int]] = 22,
        dial_time: Optional[Union[str, int]] = 60,
        cnam: Optional[Union[str, int]] = 0,
        billing_type: Optional[Union[str, int]] = 1,
    ) -> dict:
        """
        Order a local US or Canadian DID (VoIP.ms orderDID).

        Args:
            did: DID number to order (e.g. 5551234567).
            routing: Initial routing. Default 'sys:hangup'. Change later with set_did_routing.
            pop: POP server ID. Default 22 (sanjose1.voip.ms). See get_servers.
            dial_time: Ring time in seconds. Default 60.
            cnam: CNAM lookup: 0 = disabled, 1 = enabled. Default 0.
            billing_type: 1 = per minute, 2 = flat rate. Default 1.

        Returns:
            API response with the ordered DID.
        """
        
        mtd = "orderDID"

        params = {
            "did": did,
            "routing": routing,
            "pop": pop,
            "dialtime": dial_time,
            "cnam": cnam,
            "billing_type": billing_type,
        }

        data = self.get(mtd, params)
        data["result"] = "DID ordered"
        data["did"] = did
        return data

    def order_toll_free(
        self,
        did: Union[str, int],
        routing: Optional[str] = "sys:hangup",
        pop: Optional[Union[str, int]] = 22,
        dial_time: Optional[Union[str, int]] = 60,
        cnam: Optional[Union[str, int]] = 0,
    ) -> dict:
        """
        Order a toll-free US or Canadian DID (VoIP.ms orderTollFree).

        Args:
            did: Toll-free DID to order (e.g. 8771234567).
            routing: Initial routing. Default 'sys:hangup'. Change later with set_did_routing.
            pop: POP server ID. Default 22. See get_servers.
            dial_time: Ring time in seconds. Default 60.
            cnam: CNAM lookup: 0 = disabled, 1 = enabled. Default 0.

        Returns:
            API response with the ordered toll-free DID.
        """
        
        mtd = "orderTollFree"

        params = {
            "did": did,
            "routing": routing,
            "pop": pop,
            "dialtime": dial_time,
            "cnam": cnam
        }

        data = self.get(mtd, params)
        data["result"] = "DID ordered"
        data["did"] = did
        return data

    def set_did_routing(self, did: Union[str, int], routing: str) -> dict:
        """
        Set routing for a DID (VoIP.ms setDIDRouting).

        Args:
            did: DID to update (e.g. 8771234567).
            routing: Route in the form 'header:record_id'. Header can be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none (e.g. 'account:100000_SubAccount').

        Returns:
            API response with the updated DID and result message.
        """
        
        mtd = "setDIDRouting"

        params = {
            "did": did,
            "routing": routing,
        }

        data = self.get(mtd, params)
        data["did"] = did
        data["result"] = f"DID routed to {routing}"
        return data
