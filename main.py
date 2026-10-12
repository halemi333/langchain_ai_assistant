from agents.router import route_request

def main():

    print(
        "LangChain AI Assistant Started..."
    )

    while True:

        user_input = input(
            "\nUser: "
        )

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            print(
                "Goodbye!"
            )
            break

        answer = route_request(
            user_input
        )

        print(
            "\nAssistant:",
            answer
        )

if __name__ == "__main__":

    main()