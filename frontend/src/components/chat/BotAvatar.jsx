const BotAvatar = () => {
  return (
    <div
      className="w-9 h-9 rounded-full
                 bg-slate-800
                 border border-slate-600
                 flex items-center justify-center
                 overflow-hidden shrink-0"
    >
      <img
        src="/brain.png"
        alt="LLM"
        className="h-full w-full object-cover rounded-full opacity-100"
      />
    </div>
  );
};

export default BotAvatar;
