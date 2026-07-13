from search import search_prompt


def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Faça sua pergunta:")

    while True:
        try:
            question = input("PERGUNTA: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not question:
            continue

        if question.lower() in ("sair", "exit"):
            break

        try:
            answer = chain.invoke({"pergunta": question})
            print(f"RESPOSTA: {answer}")
        except Exception as exc:
            print(f"RESPOSTA: Erro ao processar a pergunta. {exc}")

        print("---")


if __name__ == "__main__":
    main()
