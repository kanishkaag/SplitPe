import {createBrowserRouter , RouterProvider} from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ManageParties from './pages/ManageParties'

import './App.css'

function App() {
  
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Login/>
    }, 
    {
      path: '/dashboard',
      element: <Dashboard/>
    }, 
    {
      path: '/admin',
      element: <ManageParties/>
    }, 
   
   
   
  ])

  return (
  


      <div className=''>
        <RouterProvider router={router}/>
      </div>
    
  )
}

export default App
