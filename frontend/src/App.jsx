import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import 'tailwindcss'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1 className='text-gray-700 dark:text-gray-400 '> Hello world</h1>
    </>
  )
}

export default App
