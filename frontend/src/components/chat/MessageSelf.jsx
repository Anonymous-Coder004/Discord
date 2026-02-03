import MessageTime from "./MessageTime";

const MessageSelf = ({ message }) => {
  return (
    <div className="flex justify-end">
      <div className="max-w-[70%] text-right">
        <div className="bg-indigo-600 px-4 py-2 rounded-xl text-white inline-block">
          {message.content}
        </div>

        <MessageTime time={message.created_at} />
      </div>
    </div>
  );
};

export default MessageSelf;
