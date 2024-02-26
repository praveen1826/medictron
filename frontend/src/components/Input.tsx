import { useState } from "react";
import axios from "axios";
import { useMessageDispatch } from "./MessageContext";

function Input() {
  const [message, setMessage] = useState("");
  const dispatch = useMessageDispatch();

  async function postMessage(message: any) {
    try {
      const data = await axios.post("http://localhost:8000/chat", {
        message,
      });

      const response = JSON.stringify(data.data);

      console.log(response);
      // console.log(response.data.output.output);
      dispatch({
        type: "added",
        id: nextId++,
        text: "Medtronic: " + JSON.parse(response).output.content,
      });
    } catch (error) {
      console.error(error);
    }
  }

  const handleSubmit = (event: any) => {
    event.preventDefault();
    postMessage(message);

    dispatch({
      type: "added",
      id: nextId++,
      text: "Human: " + message,
    });
    setMessage("");
  };

  return (
    <>
      <form
        className="d-flex flex-row align-items-center mb-1"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          className="form-control form-control-lg me-2"
          id="chatMessage"
          aria-describedby="messageHelp"
          placeholder="Enter your message here"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button type="submit" className="btn btn-primary">
          Send
        </button>
      </form>
    </>
  );
}

let nextId = 1;

export default Input;
