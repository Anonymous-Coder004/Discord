const AvatarBubble = ({ name }) => {
  const letter = name?.[0]?.toUpperCase() || "?";

  return (
    <div className="w-9 h-9 rounded-full bg-indigo-600 flex items-center justify-center text-white font-semibold shrink-0">
      {letter}
    </div>
  );
};

export default AvatarBubble;
