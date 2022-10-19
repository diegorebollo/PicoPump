# Autogenerated file
def render(session_status, msg):
    # Autogenerated file
    def render1(*a, **d):
        yield """<!DOCTYPE html>
<html lang=\"en\" data-theme=\"dark\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>PicoPump</title>
    <link rel=\"stylesheet\" href=\"https://static.drebollo.dev/PicoPump/css/pico.min.css\" />
    <link rel=\"stylesheet\" href=\"https://static.drebollo.dev/PicoPump/css/custom.css\" />
  </head>
  <body>
    <!-- Nav -->
    <nav class=\"container-fluid\">
      <ul>
        <li>
          <a href=\"/\" class=\"contrast\"><strong>PicoPump Web Tool</strong></a>
        </li>
      </ul>
      <ul>
        """
        if (session_status) is None:
            yield """    
        <li><a class=\"secondary\" href=\"/login\">Login</a></li>              
        """
        else:
            yield """        <li><a class=\"secondary\" href=\"/logout\">Logout</a></li>
        """
        yield """      </ul>
    </nav>
    <!-- Nav -->"""
    yield from render1()
    yield """    <!-- Main -->
    <main class=\"container form-container\">
      <article>
        <div class=\"form\">
          <h1>Admin Panel</h1>
          <p class=\"secondary\">"""
    yield str(msg)
    yield """</p>
          <form method=\"post\">
            <input
              autofocus=\"autofocus\"
              type=\"text\"
              name=\"user\"
              placeholder=\"Username\"
              aria-label=\"Login\"
              autocomplete=\"off\"
              required
            />
            <input
              type=\"password\"
              name=\"pwd\"
              placeholder=\"Password\"
              aria-label=\"Password\"
              autocomplete=\"off\"
              required
            />
            <button type=\"submit\" class=\"contrast\">Login</button>
          </form>
        </div>
      </article>
    </main>
    <!-- Main -->
"""
# Autogenerated file
    def render2(*a, **d):
        yield """    <!-- Footer -->
    <footer class=\"container-fluid\">
        <small
          >© 2022
          <a href=\"https://drebollo.dev\" class=\"secondary\"
            >Diego Rebollo</a
          ></small
        >
      </footer>
      <!-- ./ Footer -->
    </body>
  </html>
  """
    yield from render2()
