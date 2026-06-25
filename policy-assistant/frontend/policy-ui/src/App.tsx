import { useState, useRef, useEffect } from "react"

type Source = {
  document: string
  page: number
}

type Message = {
  role: "user" | "assistant"
  content: string
  sources?: Source[]
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement | null>(null)
  const streamBufferRef = useRef("")

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage: Message = { role: "user", content: input }

    setMessages(prev => [...prev, userMessage, { role: "assistant", content: "" }])
    setLoading(true)

    streamBufferRef.current = ""
    let buffer = ""

    const userInput = input
    setInput("")

    try {
      const response = await fetch("http://localhost:8000/api/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
      })

      const reader = response.body!.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        buffer += chunk

        const lines = buffer.split("\n")
        buffer = lines.pop() || ""

        for (let line of lines) {
          if (!line.trim()) continue

          const data = JSON.parse(line)

          if (data.type === "token") {
            streamBufferRef.current += data.content

            setMessages(prev => {
              const updated = [...prev]
              updated[updated.length - 1].content = streamBufferRef.current
              return updated
            })
          }

          if (data.type === "final") {

            console.log("FINAL EVENT:", data)

            setMessages(prev => {
              const updated = [...prev]
              updated[updated.length - 1].sources = data.sources
              return updated
            })
          }
        }
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100">

      <div className="backdrop-blur bg-white/70 border-b px-6 py-4 flex justify-between items-center shadow-sm">
        <h1 className="text-lg font-semibold text-gray-800">
          🚀 Policy Assistant
        </h1>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">

        {messages.length === 0 && (
          <div className="text-center mt-32 text-gray-400">
            <p className="text-xl font-medium mb-2">
              Ask anything about policies
            </p>
            <p className="text-sm">Start typing below 👇</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex items-end gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"
              }`}
          >
            {/* ✅ Assistant Avatar */}
            {msg.role === "assistant" && (
              <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm shadow">
                AI
              </div>
            )}

            {/* ✅ Bubble */}
            <div
              className={`
                max-w-[65%] px-4 py-3 rounded-2xl shadow-sm
                ${msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-sm"
                  : "bg-white border rounded-bl-sm text-gray-800"}
              `}
            >
              <div className="whitespace-pre-wrap">
                {msg.content}
              </div>

              {loading && i === messages.length - 1 && (
                <span className="animate-pulse ml-1">▍</span>
              )}

              {/* {msg.sources && msg.sources.length > 0 && (
                <div className="mt-3 pt-2 border-t text-xs text-gray-500">
                  <div className="font-medium text-gray-600 mb-1">
                    Sources
                  </div>

                  {msg.sources.map((s, idx) => (
                    <div key={idx} className="flex items-center gap-1">
                      📄 {" "}
                      <span className="font-medium">
                        {s.document || "Unknown"}
                      </span>
                      <span className="text-gray-400">
                        (Page {s.page ?? "-"})
                      </span>
                    </div>
                  ))}
                </div>
              )} */}
            </div>

            {msg.role === "user" && (
              <div className="w-8 h-8 rounded-full bg-gray-800 text-white flex items-center justify-center text-sm shadow">
                U
              </div>
            )}
          </div>
        ))}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t bg-white/80 backdrop-blur px-4 py-4">

        <div className="max-w-3xl mx-auto flex gap-3 items-center bg-white border rounded-2xl shadow-sm px-3 py-2">

          <input
            className="flex-1 outline-none bg-transparent px-2 py-2 text-sm"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a policy question..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />

          <button
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm transition shadow"
          >
            Send
          </button>

        </div>
      </div>
    </div>
  )
}