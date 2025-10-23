import asyncio
import httpx

API_URL = "http://localhost:8000"  
EMAIL = "user1@example.com"
PASSWORD = "user1"


async def main():
    async with httpx.AsyncClient() as client:
        # 1️⃣ Login para obter o token JWT
        print("➡️  Enviando requisição de login...")
        response = await client.post(
            f"{API_URL}/token",
            data={"username": EMAIL, "password": PASSWORD},  # OAuth2 usa 'username' e 'password'
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.status_code != 200:
            print("❌ Falha no login:", response.status_code, response.text)
            return

        token_data = response.json()
        access_token = token_data["access_token"]
        print("✅ Token recebido:", access_token)

        # 2️⃣ Requisição autenticada para o endpoint protegido
        print("\n➡️  Acessando endpoint protegido '/' ...")
        response = await client.get(
            f"{API_URL}/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code == 200:
            print("✅ Acesso permitido!")
            print("Resposta:", response.json())
        else:
            print("❌ Erro ao acessar o endpoint protegido:", response.status_code, response.text)


if __name__ == "__main__":
    asyncio.run(main())
