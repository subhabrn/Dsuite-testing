import employeeReducer, {
  setEmployees,
  setSelectedEmployee,
  addEmployee
} from '../../redux/slices/employeeSlice';

describe('Employee Slice', () => {
  const initialState = {
    employees: [],
    selectedEmployee: null,
    isLoading: false,
    error: null,
  };

  test('should handle initial state', () => {
    expect(employeeReducer(undefined, { type: 'unknown' })).toEqual(initialState);
  });

  test('should handle setEmployees', () => {
    const employees = [{ id: 1, name: 'John Doe' }];
    const actual = employeeReducer(initialState, setEmployees(employees));
    expect(actual.employees).toEqual(employees);
  });

  test('should handle setSelectedEmployee', () => {
    const employee = { id: 1, name: 'John Doe' };
    const actual = employeeReducer(initialState, setSelectedEmployee(employee));
    expect(actual.selectedEmployee).toEqual(employee);
  });

  test('should handle addEmployee', () => {
    const employee = { id: 1, name: 'John Doe' };
    const actual = employeeReducer(initialState, addEmployee(employee));
    expect(actual.employees).toEqual([employee]);
  });
});
