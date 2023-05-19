import msal

# The following two lines are here in order to prevent: asyncio.run() cannot be called from a running event loop
# See: https://github.com/jupyter/notebook/issues/3397#issuecomment-419386811
# import nest_asyncio
# nest_asyncio.apply()


def get_access_token(authority_url: str, client_id: str):
    app = msal.PublicClientApplication(authority=authority_url, client_id=client_id)

    # Start the device flow and print instructions to screen
    flow = app.initiate_device_flow(scopes=["Files.Read.All"])
    print(flow["message"])

    # Block until user logs in
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(result["error"])
