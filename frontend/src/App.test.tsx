import { render, screen } from '@testing-library/react'

import App from './App'

describe('App', () => {
  it('renders foundation banner', () => {
    render(<App />)

    expect(screen.getByText('NFL Analytics Workbench')).toBeInTheDocument()
  })
})
