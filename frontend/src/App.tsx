import "./App.css";
// import chatImg from "./assets/chat_messages.png";
import Chat from "./components/Chat";
import { MessageProvider } from "./components/MessageContext";

function App() {
  return (
    <>
      <MessageProvider>
        <Chat />
      </MessageProvider>
    </>
    // <div id="container">
    //   <h1 id="title">AI Assistant For Medical Diagnosis Using Generative AI</h1>
    //   <div id="chat">
    //     <div id="chat_history_container">
    //       <div id="chat_heading_container">
    //         <img id="chat_img" src={chatImg} />
    //         <p id="chat_history_heading">Chat History</p>
    //       </div>
    //     </div>
    //     <div id="chat_container"></div>
    //   </div>
    // </div>
  );
}

export default App;
