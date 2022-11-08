import { render } from 'react-dom'
import App from './App'
import 'bulma/css/bulma.min.css'

import { UserProvider } from './context/UserContext'

const root = document.getElementById('root')
render(
  <UserProvider>
    <App />
  </UserProvider>,
  root
)
