from flask import Flask, request, jsonify
import time

app = Flask(__name__)

def log_request():
    print("========== APP REQUEST ==========", flush=True)
    print("TIME:", time.strftime("%Y-%m-%d %H:%M:%S"), flush=True)
    print("METHOD:", request.method, flush=True)
    print("PATH:", request.path, flush=True)
    print("FULL_PATH:", request.full_path, flush=True)
    print("URL:", request.url, flush=True)
    print("HEADERS:", dict(request.headers), flush=True)

    try:
        print("JSON:", request.get_json(silent=True), flush=True)
    except Exception as e:
        print("JSON_ERROR:", str(e), flush=True)

    try:
        print("FORM:", request.form.to_dict(), flush=True)
    except Exception as e:
        print("FORM_ERROR:", str(e), flush=True)

    try:
        print("DATA:", request.get_data(as_text=True), flush=True)
    except Exception as e:
        print("DATA_ERROR:", str(e), flush=True)

    print("=================================", flush=True)


def success_response():
    return jsonify({
        "code": 0,
        "status": 1,
        "ret": 0,
        "msg": "success",
        "message": "success",
        "success": True,

        "accessToken": "ultimate-token-2099",
        "token": "ultimate-token-2099",
        "tokenExpireUnix": 2783326459,

        "endtime": "2099-12-31",
        "expire": "2099-12-31",
        "roomCode": "0000",
        "udid": "*",

        "data": {
            "endtime": "2099-12-31",
            "token": "ultimate-token-2099",
            "accessToken": "ultimate-token-2099",
            "tokenExpireUnix": 2783326459,
            "roomCode": "0000",
            "udid": "*",
            "expire": "2099-12-31",
            "features": {
                "esp": True,
                "radar": True,
                "allMaps": True,
                "enabled": True
            }
        }
    })


@app.before_request
def before_request():
    log_request()


@app.route("/", methods=["GET", "POST"])
def index():
    return success_response()


@app.route("/Auth/iOSVerify/", methods=["GET", "POST"])
def ios_verify_slash():
    return success_response()


@app.route("/Auth/iOSVerify", methods=["GET", "POST"])
def ios_verify_no_slash():
    return success_response()


@app.route("/auth/iOSVerify/", methods=["GET", "POST"])
def ios_verify_lower_auth():
    return success_response()


@app.route("/auth/iosverify/", methods=["GET", "POST"])
def ios_verify_all_lower():
    return success_response()


@app.route("/api/verify", methods=["GET", "POST"])
def api_verify():
    return success_response()


@app.route("/verify", methods=["GET", "POST"])
def verify():
    return success_response()


@app.route("/login", methods=["GET", "POST"])
def login():
    return success_response()


@app.route("/heartbeat", methods=["GET", "POST"])
def heartbeat():
    return success_response()


@app.route("/<path:any_path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def catch_all(any_path):
    print("CATCH_ALL_PATH:", any_path, flush=True)
    return success_response()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
