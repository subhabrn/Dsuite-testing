import { fetchEmployees, getEmployeeById } from '../../api/employeeService';
import axios from 'axios';

jest.mock('axios');

describe('Employee Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('fetchEmployees calls the correct API endpoint', async () => {
    const mockResponse = { data: [{ id: 1, name: 'John Doe' }] };
    axios.get.mockResolvedValueOnce(mockResponse);

    const result = await fetchEmployees();

    expect(axios.get).toHaveBeenCalledWith('/api/v1/employees');
    expect(result).toEqual(mockResponse.data);
  });

  test('getEmployeeById calls the correct API endpoint with ID', async () => {
    const mockResponse = { data: { id: 1, name: 'John Doe' } };
    axios.get.mockResolvedValueOnce(mockResponse);

    const result = await getEmployeeById(1);

    expect(axios.get).toHaveBeenCalledWith('/api/v1/employees/1');
    expect(result).toEqual(mockResponse.data);
  });
});
