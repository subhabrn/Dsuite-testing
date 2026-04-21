import apiClient from '../client';
import { Employee } from '../../types/employee';

export const getEmployees = async (): Promise<Employee[]> => {
  const response = await apiClient.get('/employees');
  return response.data;
};

export const getEmployee = async (id: string): Promise<Employee> => {
  const response = await apiClient.get(`/employees/${id}`);
  return response.data;
};

export const createEmployee = async (employee: Omit<Employee, 'id'>): Promise<Employee> => {
  const response = await apiClient.post('/employees', employee);
  return response.data;
};

export const updateEmployee = async (id: string, employee: Partial<Employee>): Promise<Employee> => {
  const response = await apiClient.put(`/employees/${id}`, employee);
  return response.data;
};

export const deleteEmployee = async (id: string): Promise<void> => {
  await apiClient.delete(`/employees/${id}`);
};
