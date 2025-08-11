from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'

@app.route('/')
def index():
    return redirect(url_for('registrarUsuario'))

@app.route('/registrarUsuario', methods=['GET', 'POST'])
def registrarUsuario():
    if 'usuarios' not in session:
        session['usuarios'] = []

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if username == '' or email == '' or password == '':
            flash('Todos os campos são obrigatórios', 'danger')
        else:
            usuarios = session['usuarios']
            usuarios.append({
                'username': username,
                'email': email,
                'password': password
            })
            session['usuarios'] = usuarios

            flash(f'Usuário {username} cadastrado com sucesso!', 'success')
            return redirect(url_for('registrarUsuario'))

    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)