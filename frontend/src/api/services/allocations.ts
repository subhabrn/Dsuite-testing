import apiClient from '../client';
import { Allocation } from '../../types/allocation';

export const getAllocations = async (): Promise<Allocation[]> => {
  const response = await apiClient.get('/allocations');
  return response.data;
};

export const getAllocation = async (id: string): Promise<Allocation> => {
  const response = await apiClient.get(`/allocations/${id}`);
  return response.data;
};

export const createAllocation = async (allocation: Omit<Allocation, 'id'>): Promise<Allocation> => {
  const response = await apiClient.post('/allocations', allocation);
  return response.data;
};

export const updateAllocation = async (id: string, allocation: Partial<Allocation>): Promise<Allocation> => {
  const response = await apiClient.put(`/allocations/${id}`, allocation);
  return response.data;
};

export const deleteAllocation = async (id: string): Promise<void> => {
  await apiClient.delete(`/allocations/${id}`);
};
