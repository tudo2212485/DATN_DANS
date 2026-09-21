'use client';

import { getUser } from '@/lib/auth';
import React, { useState, useEffect } from 'react';
import {
  fetchAdminUsersApi,
  createAdminUserApi,
  updateUserRoleApi,
  toggleUserStatusApi,
} from '@/lib/api';
import { AdminUserItem } from '@/types';
import {
  Users,
  UserPlus,
  ShieldCheck,
  RefreshCw,
  CheckCircle2,
  Lock,
  Unlock,
  AlertCircle,
} from 'lucide-react';

export default function DashboardUsersPage() {
  const currentUserId = getUser()?.id;
  const [busy, setBusy] = useState(false);
  const [users, setUsers] = useState<AdminUserItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [userModalOpen, setUserModalOpen] = useState(false);
  const [userForm, setUserForm] = useState({
    email: '',
    password: '',
    full_name: '',
    role: 'analyst',
  });
  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await fetchAdminUsersApi();
      setUsers(data);
    } catch (e) {
      setUsers([]);
      setToastMessage({text: e instanceof Error ? e.message : 'Không tải được tài khoản', type: 'error'});
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      await createAdminUserApi(userForm);
      setUserModalOpen(false);
      setUserForm({ email: '', password: '', full_name: '', role: 'analyst' });
      setToastMessage({ text: 'Đã tạo người dùng mới thành công', type: 'success' });
      await loadUsers();
    } catch (err: unknown) {
      setToastMessage({ text: err instanceof Error ? err.message : 'Không thể tạo người dùng', type: 'error' });
    } finally { setBusy(false); }
  };

  const handleRoleChange = async (userId: number, newRole: string) => {
    setBusy(true);
    try {
      await updateUserRoleApi(userId, newRole);
      setToastMessage({ text: `Đã cập nhật quyền thành '${newRole}' thành công`, type: 'success' });
      await loadUsers();
    } catch (err: unknown) {
      setToastMessage({ text: err instanceof Error ? err.message : 'Không thể đổi quyền', type: 'error' });
    } finally { setBusy(false); }
  };

  const handleToggleStatus = async (userId: number) => {
    setBusy(true);
    try {
      const res = await toggleUserStatusApi(userId);
      setToastMessage({ text: res.message || 'Đã thay đổi trạng thái tài khoản', type: 'success' });
      await loadUsers();
    } catch (err: unknown) {
      setToastMessage({ text: err instanceof Error ? err.message : 'Không thể thay đổi trạng thái', type: 'error' });
    } finally { setBusy(false); }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
        <div>
          <h1 className="text-2xl font-bold text-primary-text flex items-center gap-2.5">
            <Users className="w-6 h-6 text-brand" />
            Quản Lý Tài Khoản & Phân Quyền Người Dùng
          </h1>
          <p className="text-sm text-secondary-text mt-1">
            Cấp quyền Admin / Analyst, phân bổ vai trò và quản lý trạng thái tài khoản
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadUsers}
            disabled={loading}
            className="px-3.5 py-2 rounded-xl bg-card hover:bg-canvas text-secondary-text border border-border-subtle text-xs font-semibold flex items-center gap-2 transition shadow-xs"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Làm Mới
          </button>

          <button
            onClick={() => setUserModalOpen(true)}
            className="px-3.5 py-2 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-semibold flex items-center gap-1.5 shadow-xs transition"
          >
            <UserPlus className="w-3.5 h-3.5" />
            Tạo Người Dùng Mới
          </button>
        </div>
      </div>

      {/* Toast message */}
      {toastMessage && (
        <div
          className={`p-4 rounded-xl text-xs font-medium flex items-center justify-between border ${
            toastMessage.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
              : 'bg-rose-50 text-rose-800 border-rose-200'
          }`}
        >
          <div className="flex items-center gap-2">
            {toastMessage.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            ) : (
              <AlertCircle className="w-4 h-4 text-rose-600" />
            )}
            <span>{toastMessage.text}</span>
          </div>
          <button onClick={() => setToastMessage(null)} className="text-secondary-text hover:text-primary-text">
            ✕
          </button>
        </div>
      )}

      {/* Users Table */}
      <div className="p-6 rounded-2xl bg-card border border-border-subtle shadow-xs space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
          <span className="font-semibold text-primary-text text-sm flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-brand" />
            Danh Sách Tài Khoản Trong Hệ Thống ({users.length})
          </span>
          <span className="text-xs text-secondary-text font-medium">RBAC Enabled</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-primary-text">
            <thead className="bg-canvas text-secondary-text uppercase text-[11px] font-semibold border-b border-border-subtle">
              <tr>
                <th className="py-3 px-4">ID</th>
                <th className="py-3 px-4">Họ Và Tên</th>
                <th className="py-3 px-4">Email Đăng Nhập</th>
                <th className="py-3 px-4">Vai Trò (Role)</th>
                <th className="py-3 px-4">Trạng Thái</th>
                <th className="py-3 px-4 text-right">Hành Động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {users.map((u) => {
                const isDisabled = u.isActive === false || u.role.includes('_disabled');
                const baseRole = u.role.replace('_disabled', '');
                return (
                  <tr key={u.id} className="hover:bg-canvas/60 transition">
                    <td className="py-3.5 px-4 font-mono text-secondary-text">#{u.id}</td>
                    <td className="py-3.5 px-4 font-medium text-primary-text">{u.fullName}</td>
                    <td className="py-3.5 px-4 font-mono text-secondary-text">{u.email}</td>
                    <td className="py-3.5 px-4">
                      <select
                        disabled={busy || u.id === currentUserId} value={baseRole}
                        onChange={(e) => handleRoleChange(u.id, e.target.value)}
                        className="bg-canvas border border-border-subtle text-xs text-primary-text rounded-lg px-2.5 py-1 focus:outline-none focus:border-brand"
                      >
                        <option value="admin">Quản trị viên (Admin)</option>
                        <option value="analyst">Nhà phân tích (Analyst)</option>
                        <option value="user">Người dùng (User)</option>
                      </select>
                    </td>
                    <td className="py-3.5 px-4">
                      {isDisabled ? (
                        <span className="px-2 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-[10px] font-semibold">
                          Đã Khóa
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-semibold">
                          Hoạt Động
                        </span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        disabled={busy || u.id === currentUserId} onClick={() => handleToggleStatus(u.id)}
                        className={`p-1.5 rounded-lg text-xs transition ${
                          isDisabled
                            ? 'text-brand hover:bg-brand-light'
                            : 'text-rose-600 hover:bg-rose-50'
                        }`}
                        title={isDisabled ? 'Mở khóa tài khoản' : 'Khóa tài khoản'}
                      >
                        {isDisabled ? <Unlock className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal: Tạo Người Dùng Mới */}
      {userModalOpen && (
        <div className="fixed inset-0 z-50 bg-primary-text/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-card border border-border-subtle rounded-2xl p-6 space-y-4 shadow-xl">
            <h3 className="text-lg font-bold text-primary-text flex items-center gap-2">
              <UserPlus className="w-5 h-5 text-brand" />
              Tạo Người Dùng Hệ Thống
            </h3>

            <form onSubmit={handleCreateUser} className="space-y-3.5 text-xs">
              <div>
                <label className="block text-secondary-text font-medium mb-1">Họ và Tên</label>
                <input
                  type="text"
                  value={userForm.full_name}
                  onChange={(e) => setUserForm({ ...userForm, full_name: e.target.value })}
                  placeholder="VD: Nguyễn Văn A"
                  className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                  required
                />
              </div>

              <div>
                <label className="block text-secondary-text font-medium mb-1">Email Đăng Nhập</label>
                <input
                  type="email"
                  value={userForm.email}
                  onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                  placeholder="VD: analyst@agroforecast.vn"
                  className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                  required
                />
              </div>

              <div>
                <label className="block text-secondary-text font-medium mb-1">Mật Khẩu</label>
                <input
                  type="password"
                  value={userForm.password}
                  onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
                  placeholder="Tối thiểu 6 ký tự"
                  className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                  required
                />
              </div>

              <div>
                <label className="block text-secondary-text font-medium mb-1">Phân Quyền (Role)</label>
                <select
                  value={userForm.role}
                  onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}
                  className="w-full bg-canvas border border-border-subtle rounded-xl px-3 py-2 text-primary-text"
                >
                  <option value="analyst">Nhà phân tích (Analyst)</option>
                  <option value="admin">Quản trị viên (Admin)</option>
                  <option value="user">Người dùng thông thường (User)</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-border-subtle">
                <button
                  type="button"
                  onClick={() => setUserModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-canvas border border-border-subtle text-secondary-text font-medium hover:bg-[#EFECE6] transition"
                >
                  Hủy Bỏ
                </button>
                <button
                  type="submit" disabled={busy}
                  className="px-4 py-2 rounded-xl bg-brand hover:bg-brand-hover text-white font-semibold shadow-xs transition"
                >
                  Tạo Người Dùng
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
