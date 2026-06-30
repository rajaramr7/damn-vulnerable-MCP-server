"""Billing MCP server: exposes billing tools to the model over MCP.

This file is the payload for the demonstration pull request. It introduces a
NEW in-house MCP server whose tools include a financial action (issue_refund)
and a destructive action (delete_account), with no human-approval gate. That is
net-new high-risk AI surface, so the ai-surface CI gate fails the PR and comments
the finding, while the repo's pre-existing MCP servers (already on the base
branch) are left untouched.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("billing-mcp")


@mcp.tool()
def get_invoice(invoice_id: str) -> dict:
    """Read an invoice by id."""
    return {"invoice_id": invoice_id}


@mcp.tool()
def issue_refund(order_id: str, amount: float) -> dict:
    """Issue a refund against an order. Runs with no approval step."""
    return {"refund_id": "r_1"}


@mcp.tool()
def delete_account(customer_id: str) -> dict:
    """Hard-delete a customer account and all associated data."""
    return {"deleted": True}


if __name__ == "__main__":
    mcp.run()
