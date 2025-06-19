from werkzeug.security import generate_password_hash

senha = "octavio1234"
hash_senha = generate_password_hash(senha, method='pbkdf2:sha256')
print(f"Hash gerado: {hash_senha}")
print("\nPara atualizar no banco, use:")
print(f"UPDATE usuarios SET senha_hash = '{hash_senha}' WHERE email = 'octavio@eshows.com.br';")