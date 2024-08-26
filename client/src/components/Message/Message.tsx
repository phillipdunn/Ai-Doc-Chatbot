import React, { FC } from 'react';

interface Props {
  key: number;
  position: string;
  message: string;
}

const Message: FC<Props> = ({ key, message, position }) => {
  let dataRoll = position === "left_bubble" ? "ASSISTANT" : "USER";
  let thisClass = `chat-bubble ${position}`;
  return (
    <div data-role={dataRoll} className="bubble-container">
      <div className={thisClass}>
        <div className="text_message">
          {message?.replace(/<\/?[^>]+(>|$)/g, "")}
        </div>
      </div>
      <div className="clear"></div>
    </div>
  );
};

export default Message;
