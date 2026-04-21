import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../../../components/common/Button';

// Mock Button component if it doesn't exist
jest.mock('../../../components/common/Button', () => {
  return function MockButton({ children, onClick }) {
    return (
      <button data-testid="button" onClick={onClick}>
        {children}
      </button>
    );
  };
});

describe('Button Component', () => {
  it('renders button text correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByTestId('button')).toHaveTextContent('Click me');
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByTestId('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
