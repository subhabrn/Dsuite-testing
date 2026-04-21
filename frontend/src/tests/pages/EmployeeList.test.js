import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import EmployeeList from '../../pages/EmployeeList';
import { fetchEmployees } from '../../redux/slices/employeeSlice';

jest.mock('../../redux/slices/employeeSlice', () => ({
  fetchEmployees: jest.fn(),
}));

const mockStore = configureStore([thunk]);

describe('EmployeeList Page', () => {
  let store;

  beforeEach(() => {
    store = mockStore({
      employees: {
        employees: [
          { id: 1, name: 'John Doe', position: 'Developer' },
          { id: 2, name: 'Jane Smith', position: 'Designer' }
        ],
        isLoading: false,
        error: null
      }
    });
    fetchEmployees.mockReturnValue({ type: 'employees/fetchEmployees' });
  });

  test('renders employee list with data', () => {
    render(
      <Provider store={store}>
        <EmployeeList />
      </Provider>
    );

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
  });

  test('dispatches fetchEmployees on mount', () => {
    render(
      <Provider store={store}>
        <EmployeeList />
      </Provider>
    );

    expect(fetchEmployees).toHaveBeenCalledTimes(1);
  });

  test('shows loading state', () => {
    const loadingStore = mockStore({
      employees: {
        employees: [],
        isLoading: true,
        error: null
      }
    });

    render(
      <Provider store={loadingStore}>
        <EmployeeList />
      </Provider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});
