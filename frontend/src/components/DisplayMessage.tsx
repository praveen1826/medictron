import { useMessage } from "./MessageContext";

function DisplayMessage() {
  const messages = useMessage();
  return (
    <>
      {messages.map((message) => (
        <p key={message.id}>{message.text}</p>
      ))}
    </>
  );
}

export default DisplayMessage;
