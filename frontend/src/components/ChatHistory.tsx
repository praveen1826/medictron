import chatImg from "../assets/chat_messages.png";

function ChatHistory() {
  return (
    <div
      id="chat_history_container"
      className="col-3 border me-2 d-md-block d-none"
    >
      <div
        id="chat_heading_container"
        className="d-flex justify-content-center align-items-center flex-row border"
      >
        <img id="chat_img" src={chatImg} />

        <p id="chat_history_heading" className="mb-0">
          Chat History
        </p>
      </div>
    </div>
  );
}

export default ChatHistory;
