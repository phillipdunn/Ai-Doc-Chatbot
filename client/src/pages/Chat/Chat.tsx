import React, { FC, useState } from 'react';
import SVG from '../../components/SVG';
import AdbIcon from '@mui/icons-material/Adb';
import Message from '../../components/Message';
import './Chat.scss';
import { Box, Typography } from '@mui/material';
interface Props { }

const Chat: FC<Props> = () => {

  // this function opens the chat
  function openChart() {
    document.getElementById("assistant-chat")?.classList.add("show");
    document.getElementById("assistant-chat")?.classList.remove("hide");
  }

  // this function opens the chat
  function closeChart() {
    document.getElementById("assistant-chat")?.classList.add("hide");
    document.getElementById("assistant-chat")?.classList.remove("show");
  }

  function chat_scroll_up() {
    let elem = document.querySelector(".start-chat");
    setTimeout(() => {
      elem?.scrollTo({
        top: elem.scrollHeight,
        behavior: "smooth",
      });
    }, 200);
  }

  const [chatMessages, setChatMessages] = useState([
    {
      position: "left_bubble",
      message: "Hello,I am Doc chatbot. How can i help you? ",
    },
  ]);

  function askAI() {
    var prompt_input = document.getElementById("chat-input") as HTMLInputElement;
    var prompt = prompt_input?.value;
    if (prompt.replaceAll(" ", "") === "") {
      return;
    }
    prompt_input.value = "";

    const data = {
      chatHistory: JSON.stringify(chatMessages),
      prompt: prompt,
    };

    fetch("/ask_ai", {
      method: "POST",
      body: JSON.stringify(data), // Convert data to JSON
      headers: {
        "Content-Type": "application/json", // Set the content type to JSON
      },
    })
      .then((response) => response.json())

      .then((resData: any) => {
        console.log(resData)
        const messages = [
          ...chatMessages,
          {
            position: "right_bubble",
            message: prompt,
          },
          {
            position: "left_bubble",
            message: resData?.result,
          },
        ];
        setChatMessages(messages);
        chat_scroll_up()
      })
      .catch((err) => console.log(err));
  }

  return (
    <div>
      <div>
        <div id="assistant-chat" className="hide ai_chart">
          <Box className="chatbotAvatar">
            <AdbIcon />
          </Box>
          <Typography>
            <span className="chatbotName">Doc Chatbot</span>
            <br />
            <small>Online</small>
          </Typography>
          <div className="start-chat">
            <div className="assistant-chat-body">
              {chatMessages.map((chatMessage: { position: string; message: string; }, key: number) => (
                <Message
                  key={key}
                  position={chatMessage.position}
                  message={chatMessage.message}
                />
              ))}
            </div>
            <div className="blanter-msg">
              <input
                type="text"
                id="chat-input"
                placeholder="type here..."
                maxLength={400}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    askAI();
                  }
                }}
              />
              <a
                onClick={askAI}
                href="#send_message"
                id="send-it"
                className="send_it"
              >
                <svg viewBox="0 0 448 448">
                  <path d="M.213 32L0 181.333 320 224 0 266.667.213 416 448 224z" />
                </svg>
              </a>
            </div>
          </div>
          <a className="close-chat" href="#close" onClick={closeChart}>
            &times;
          </a>
        </div>
        <a
          onClick={openChart}
          className="blantershow-chat"
          href="#load_chart"
          title="Show Chat"
        >
          <AdbIcon />
          Chat to your document
        </a>
      </div>
    </div>
  );
};

export default Chat;
