from flask import Flask, render_template, request, session, redirect, url_for, make_response
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(10)

users = {
    "Usuário1": "fabio",
    "Usuário2": "cirilo",
}

@app.route("/")
def homepage():
    session['acessos'] = session.get('acessos', 0) + 1

    logado = 'username' in session
    if logado:
        return redirect(url_for('profile', username=session['username']))
    else:
        return render_template('login.html',
                            logado=logado,
                            acessos=session['acessos'])


@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    senha = request.form['senha']
    
    if username in users and users[username] == senha:
        session['username'] = username
        return redirect(url_for('profile', username=username))
    else:
        logado = False
        msg = "*Usuário ou senha inválidos"
        return render_template('login.html',
                            logado=logado,
                            msg=msg,
                            acessos=session.get('acessos', 0))


@app.route("/profile")
def profile_redirecionar():
    if 'username' in session:
        return redirect(url_for('profile', username=session['username']))
    else:
        return redirect(url_for('homepage'))


@app.route("/user/<username>")
def profile(username):
    if 'username' in session and session['username'] == username:
        filtro = request.cookies.get('filtro', 'todas')
        tema = request.cookies.get('tema', 'claro')
        return render_template('profile.html',
                        user=username,
                        acessos=session.get('acessos', 0),
                        filtro_atual=filtro,
                        tema=tema)
    else:
        return redirect(url_for('homepage'))

@app.route("/set_filtro/<categoria>")
def set_filtro(categoria):
    if 'username' not in session:
        return redirect(url_for('homepage'))

    categorias_validas = ['todas', 'esportes', 'lazer', 'entretenimento']
    categoria = categoria.lower()
    if categoria not in categorias_validas:
        categoria = 'todas'
    
    resp = make_response(redirect(url_for('profile', username=session['username'])))
    resp.set_cookie('filtro', categoria)
    return resp

@app.route("/set_tema/<tema>")
def set_tema(tema):
    if tema.lower() not in ['claro', 'escuro']:
        tema = 'claro'

    resposta = make_response(redirect(request.referrer or url_for('homepage')))
    resposta.set_cookie('tema', tema.lower(), max_age=60*10)
    return resposta

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('acessos', None)
    return redirect(url_for('homepage'))


if __name__ == "__main__":
    app.run(debug=True)