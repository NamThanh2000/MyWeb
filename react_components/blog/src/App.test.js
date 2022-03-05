import { render, screen } from '@testing-library/react';
import AppBlogForm from './AppBlogForm';

test('renders learn react link', () => {
  render(<AppBlogForm />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
