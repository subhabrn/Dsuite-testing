import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../../components/common/Button';

describe('Button Component', () => {
  test('renders button with correct text', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('applies custom className when provided', () => {
    render(<Button className="custom-class">Click Me</Button>);
    expect(screen.getByText('Click Me')).toHaveClass('custom-class');
  });
});
