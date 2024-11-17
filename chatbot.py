import streamlit as st
import openai

# OpenAI API Key
openai.api_key = "API"  # Replace with your OpenAI API key

# Function to interact with OpenAI API
def query_openai(messages, max_tokens=300, temperature=0.7, top_p=0.9):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if GPT-4 is unavailable
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
def main():
    st.title("Crypto Assistant with Chat History and Controls")
    st.markdown(
        "Interact with a cryptocurrency expert! Ask about blockchain, trading, tokenomics, security, and more."
    )

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": [
                {
                "type": "text",
                "text": "You are a cryptocurrency expert who wants to mentor beginner-level traders on their crypto trading journey. You want to give them considered yet helpful information regarding their queries. you will be enthusiastic in your response and assist them with only and exclusively crypto-related questions. If the question is out of context, respond by saying, \"Sorry, I can't tell you that, but I am here for all your crypto queries.\"  you will always live then with additional material from the web to explore on your own.\n"
                }
            ]
            }
        ]
    if "show_history" not in st.session_state:
        st.session_state.show_history = False  # Toggle for showing more/less chat history

    # User input
    user_query = st.text_input("Type your question here:")

    # Buttons for interaction
    col1, col2 = st.columns([1, 1])
    with col1:
        send_query = st.button("Send")
    with col2:
        clear_chat = st.button("Clear Chat")

    # Clear chat history
    if clear_chat:
        st.session_state.messages = [
            {"role": "system", "content": (
                "You are a cryptocurrency expert trained to provide detailed and accurate answers. "
                "Focus on blockchain technology, trading, tokenomics, security, and cryptocurrency regulations. "
                "When possible, provide examples and use clear, concise language. Avoid providing financial advice."
            )}
        ]
        st.session_state.show_history = False
        st.success("Chat history cleared.")

    # Process user query
    if send_query and user_query.strip():
        # Add user query to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Generate response from OpenAI
        with st.spinner("Generating response..."):
            response = query_openai(st.session_state.messages)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Automatically expand history after a query
        st.session_state.show_history = True

    # Display chat history with show more/less toggle
    st.subheader("Chat History")
    if st.session_state.show_history:
        for i, msg in enumerate(st.session_state.messages[1:]):  # Exclude system message
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"**Crypto Assistant:** {msg['content']}")

        if st.button("Show Less"):
            st.session_state.show_history = False
    else:
        # Show the last two messages (most recent user and assistant exchange)
        last_msgs = st.session_state.messages[-2:] if len(st.session_state.messages) > 2 else st.session_state.messages
        for msg in last_msgs:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"**Crypto Assistant:** {msg['content']}")

        if st.button("Show More"):
            st.session_state.show_history = True

    # Sidebar with parameters
    st.sidebar.title("Settings")
    max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 300, step=50)
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, step=0.1)
    top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.9, step=0.1)
    st.sidebar.markdown(
        """
        - **Max Tokens**: Controls the length of the response.
        - **Temperature**: Higher values make the output more random.
        - **Top P**: Nucleus sampling to limit the token selection pool.
        """
    )

    # Update parameters dynamically
    if st.sidebar.button("Update Settings"):
        response = query_openai(
            st.session_state.messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        st.sidebar.success("Settings updated!")

# Run the app
if __name__ == "__main__":
    main()
