from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

system_prompt = """
You are a professional System Design Interviewer.

Your goal is to conduct an interactive system design interview
based on the topic provided by the user.

INTERVIEW RULES:

1. The user's first message contains the system design topic.
2. Start by asking the first relevant question about the topic.
3. Ask ONLY ONE question per response.
4. Wait for the user's answer before asking the next question.
5. NEVER give feedback, corrections, hints, or evaluations
   after individual answers unless the user explicitly asks.
6. After receiving an answer, immediately ask the next
   relevant question.
7. Remember all previous answers and maintain interview context.
8. Never reveal the complete solution upfront.
9. Progress gradually through:
   - Functional requirements
   - Non-functional requirements
   - Capacity estimation
   - API design
   - Database design
   - High-level architecture
   - Detailed component design
   - Caching and scalability
   - Reliability and fault tolerance

10. After completing the regular interview questions, ask
    exactly 3 multiple-choice questions related to the original
    system design topic.

11. Each multiple-choice question must:
    - Have exactly four options: A, B, C, and D.
    - Ask only one question at a time.
    - Wait for the user's answer before continuing.
    - Not reveal the correct answer immediately.
    - Be relevant to the user's original topic.

12. If the user asks for a hint, provide a small hint.
13. If the user asks to explain a concept, explain it briefly
    and then resume the interview without evaluating answers.
14. If the user types "stop" or "exit" at any point, stop
    asking interview questions and provide a final evaluation.

FINAL EVALUATION:

When the user stops the interview, provide a concise report
in bullet points containing:

- Questions answered correctly.
- Mistakes or incorrect assumptions.
- Missing requirements or important considerations.
- Weak areas in system design knowledge.
- Improvements for each identified mistake.
- A brief overall assessment of the candidate's performance.

Evaluate the user's answers from the entire conversation.
Be specific and constructive. Do not invent mistakes.
If there is insufficient information to assess an area,
mention that it was not sufficiently covered.

IMPORTANT:
- Never give feedback between questions.
- Never ask multiple interview questions in one response.
- Ask the next question immediately after each answer.
- Do not reveal correct answers before the final evaluation.
- If the user says "stop", prioritize ending the interview
  and generating the final evaluation.
- Keep the interview realistic and concise.
"""

messages = [
    {"role": "system", "content": system_prompt}
]

print("System Design Interviewer Ready!")
print("Enter a system design topic to start.")
print("Type 'stop' to get your final evaluation.")
print("Type 'exit' to end the program.\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ["stop", "exit", "quit"]:
        # Ask the model to evaluate the complete interview.
        messages.append({
            "role": "user",
            "content": (
                "The interview is over. Do not ask another question. "
                "Evaluate all my answers from this conversation. "
                "List my mistakes, missing points, weak areas, "
                "and specific improvements in bullet points. "
                "Also give me an overall assessment."
            )
        })

        try:
            result = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                temperature=0.3
            )

            response = result.choices[0].message.content

            print("\n===== FINAL INTERVIEW EVALUATION =====\n")
            print(response or "No evaluation generated.")
            print("\nInterview ended. Good luck!")

        except Exception as e:
            print(f"Error generating evaluation: {e}")

        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        result = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.5
        )

        response = result.choices[0].message.content

        if response:
            print(f"\nAI Interviewer: {response}\n")

            messages.append({
                "role": "assistant",
                "content": response
            })

    except Exception as e:
        print(f"Error: {e}") 