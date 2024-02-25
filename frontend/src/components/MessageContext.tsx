import React, { createContext, useContext, useReducer } from "react";

interface Message {
  id: number;
  text: string;
  done: boolean;
}

type Action = { type: "added"; id: number; text: string };

const MessageContext = createContext<Message[]>([]);
const MessageDispatchContext = createContext<React.Dispatch<Action>>(() => {});

export function MessageProvider({ children }: { children: React.ReactNode }) {
  const [messages, dispatch] = useReducer(messageReducer, initialMessage);

  return (
    <MessageContext.Provider value={messages}>
      <MessageDispatchContext.Provider value={dispatch}>
        {children}
      </MessageDispatchContext.Provider>
    </MessageContext.Provider>
  );
}

export function useMessage() {
  return useContext(MessageContext);
}

export function useMessageDispatch() {
  return useContext(MessageDispatchContext);
}

function messageReducer(messages: Message[], action: Action): Message[] {
  switch (action.type) {
    case "added": {
      return [
        ...messages,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];
    }

    default: {
      throw Error("Unknown action: " + action.type);
    }
  }
}

const initialMessage: Message[] = [
  { id: 0, text: "Medtronic: Hello, How May I Help You", done: true },
];
