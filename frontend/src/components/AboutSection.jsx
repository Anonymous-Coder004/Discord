import React from "react";

const AboutSection = () => {
  return (
    <div className="relative flex flex-1 items-center justify-center overflow-hidden">
      {/* Center content */}
      <div className="text-center px-6">
        <h1 className="text-4xl md:text-5xl font-semibold text-white tracking-wide">
          Welcome aboard to Devcord!
        </h1>

        <p className="mt-4 text-lg md:text-xl text-gray-300">
          LLM based community for developers
        </p>

        <p className="mt-6 text-sm md:text-base text-gray-400">
          Create or Select a Room to continue
        </p>
      </div>

      {/* Footer / License */}
      <div className="absolute bottom-4 text-xs text-gray-500">
        Licensed by Devcord Team
      </div>
    </div>
  );
};

export default AboutSection;
