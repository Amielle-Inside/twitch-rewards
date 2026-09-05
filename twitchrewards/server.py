""""Starts uvicorn server for the app."""

import uvicorn

from twitchrewards.config import settings

if __name__ == "__main__":
    # Check if SSL certificates exist
    import os
    ssl_keyfile = settings.SSL_KEY_PATH if os.path.exists(settings.SSL_KEY_PATH) else None
    ssl_certfile = settings.SSL_CERTIFICATE_PATH if os.path.exists(settings.SSL_CERTIFICATE_PATH) else None
    
    # Always run on port 5151 internally; APP_PORT is for URL generation only
    uvicorn.run(
        "twitchrewards.main:app",
        host="0.0.0.0",
        port=5151,
        reload=True,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
    )
