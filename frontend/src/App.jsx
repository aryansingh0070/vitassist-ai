import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(
          userQuestion
        )}`
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.answer || "No response received",
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "❌ Backend connection failed",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "20px auto",
        padding: "20px",
        fontFamily: "Arial",
      }}
    >
      <h1>🎓 VITAssist AI</h1>

      <div
        style={{
          minHeight: "450px",
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "15px",
          marginBottom: "20px",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign:
                msg.role === "user"
                  ? "right"
                  : "left",
              marginBottom: "15px",
            }}
          >
            <b>
              {msg.role === "user"
                ? "You"
                : "VITAssist"}
            </b>

            <div>{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div>
            <b>VITAssist</b>
            <div>🤔 Thinking...</div>
          </div>
        )}
      </div>

      <input
        type="text"
        value={question}
        placeholder="Ask anything..."
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            askQuestion();
          }
        }}
        style={{
          width: "75%",
          padding: "12px",
        }}
      />

      <button
        onClick={askQuestion}
        style={{
          padding: "12px",
          marginLeft: "10px",
          cursor: "pointer",
        }}
      >
        Send
      </button>
    </div>
  );
}

export default App;