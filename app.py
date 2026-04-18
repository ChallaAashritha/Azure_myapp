import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template


app = Flask(__name__)


def get_env_settings():
    """Read application settings from environment variables."""
    return {
        "app_name": os.getenv("APP_NAME", "Azure Env Demo"),
        "app_environment": os.getenv("APP_ENVIRONMENT", "development"),
        "app_owner": os.getenv("APP_OWNER", "team"),
        "feature_message": os.getenv(
            "FEATURE_MESSAGE",
            "Configure FEATURE_MESSAGE in Azure App Service to change this text.",
        ),
        "show_debug_details": os.getenv("SHOW_DEBUG_DETAILS", "false").lower() == "true",
    }


@app.route("/")
def home():
    settings = get_env_settings()
    return render_template("index.html", settings=settings)


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.route("/api/app-info")
def app_info():
    settings = get_env_settings()
    return jsonify(
        {
            "application": {
                "name": settings["app_name"],
                "environment": settings["app_environment"],
                "owner": settings["app_owner"],
            },
            "runtime": {
                "python_version": os.sys.version,
                "server_port": os.getenv("PORT", "5000"),
            },
            "azure_app_service": {
                "site_name": os.getenv("WEBSITE_SITE_NAME", "not-set"),
                "instance_id": os.getenv("WEBSITE_INSTANCE_ID", "not-set"),
                "resource_group": os.getenv("WEBSITE_RESOURCE_GROUP", "not-set"),
                "region": os.getenv("REGION_NAME", "not-set"),
            },
            "available_endpoints": {
                "home": "/",
                "health": "/health",
                "app_info": "/api/app-info",
                "env_showcase": "/api/env-showcase",
            },
        }
    )


@app.route("/api/env-showcase")
def env_showcase():
    settings = get_env_settings()
    return jsonify(
        {
            "message": "Environment variables loaded successfully.",
            "configured_values": {
                "APP_NAME": settings["app_name"],
                "APP_ENVIRONMENT": settings["app_environment"],
                "APP_OWNER": settings["app_owner"],
                "FEATURE_MESSAGE": settings["feature_message"],
                "SHOW_DEBUG_DETAILS": settings["show_debug_details"],
            },
            "azure_note": (
                "Set these keys in Azure App Service under Settings > Environment variables."
            ),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=get_env_settings()["show_debug_details"])
