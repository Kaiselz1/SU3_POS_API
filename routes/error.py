from app import app, jsonify   

@app.errorhandler(403)
def error_403(e):
    return jsonify ({
        "status": 403,
        "message": "Forbidden access" 
    }), 403

@app.errorhandler(404)
def error_404(e):
    return jsonify ({
        "status": 404,
        "message": "Page not found"
    }), 404

@app.errorhandler(500) 
def error_500(e):
    return jsonify ({
        "status": 500,
        "message": "Internal server error",
        # "details": str(e)   
    }), 500

# @app.errorhandler(Exception)
# def error_exception(e):
#     return jsonify ({
#         "message": str(e)
#     })