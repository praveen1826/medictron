import "./Chat.css";
import ChatHistory from "./ChatHistory";
import DisplayMessage from "./DisplayMessage";
import Input from "./Input";

function Chat() {
  return (
    <>
      <div
        id="container"
        className="d-flex container-fluid overflow-auto flex-column"
      >
        <div className="row">
          <h1 id="title" className="text-center">
            AI Assistant For Medical Diagnosis Using Large Language Models
          </h1>
        </div>
        <div
          id="chat"
          className="row gx-2 d-flex justify-content-center m-md-3 m-2 "
        >
          <ChatHistory />

          <div
            id="chat_container"
            className="d-flex col-md-8 col-12 border ms-2 overflow-hidden"
          >
            <div className="d-md-none position-absolute border">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                className="bi bi-list"
                viewBox="0 0 16 16"
              >
                <path
                  fill-rule="evenodd"
                  d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"
                />
              </svg>
            </div>
            <div className="mt-auto flex-grow-1">
              <div style={{ maxHeight: "80vh", overflowY: "auto" }}>
                <DisplayMessage />
              </div>

              <Input />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Chat;
