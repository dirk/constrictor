Error_404 = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL {path} was not found on this server.</p>
</body></html>
"""
Redirect = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>{status} Redirect</title>
</head><body>
<h1>Redirect</h1>
<p>Your are being redirected to "<a href="{path}">{path}</a>".</p>
</body></html>
"""