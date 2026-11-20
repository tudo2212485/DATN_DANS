'use client';

import { getUser } from '@/lib/auth';
import React, { useState, useEffect, useMemo } from 'react';
import AgroGrid, { AgroColumn } from '@/components/ui/AgroGrid';
import {
  fetchAdminUsersApi,
  createAdminUserApi,
  updateUserRoleApi,
  toggleUserStatusApi,
} from '@/lib/api';
import { AdminUserItem } from '@/types';
import {
  UserPlus,
  RefreshCw,
  CheckCircle2,
  Lock,
  Unlock,
  AlertCircle,
} from 'lucide-react';

const ROLE_OPTIONS = [
  { value: 'admin', label: 'Quản trị viên (Admin)' },
  { value: 'analyst', label: 'Chuyên viên phân tích (Analyst)' },
  { value: 'user', label: 'Người dùng (User)' },
] as const;

function getRoleLabel(baseRole: string): string {
  const matched = ROLE_OPTIONS.find((r) => r.value === baseRole);
  return matched ? matched.label : 'Người dùng (User)';
}

export default function DashboardUsersPage() {
  const currentUserId = getUser()?.id;
  const [busy, setBusy] = useState(false);
  const [users, setUsers] = useState<AdminUserItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [userModalOpen, setUserModalOpen] = useState(false);
  const [roleFilter, setRoleFilter] = useState<string>('ALL');
  const [modalError, setModalError] = useState('');

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
      setToastMessage({
        text: e instanceof Error ? e.message : 'Không tải được danh sách tài khoản',
        type: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadUsers();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setModalError('');

    if (!userForm.full_name.trim()) {
      setModalError('Vui lòng nhập họ và tên.');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userForm.email.trim())) {
      setModalError('Địa chỉ email không đúng định dạng.');
      return;
    }
    if (userForm.password.length < 6) {
      setModalError('Mật khẩu phải có tối thiểu 6 ký tự.');
      return;
    }

    setBusy(true);
    try {
      await createAdminUserApi({
        ...userForm,
        email: userForm.email.trim(),
        full_name: userForm.full_name.trim(),
      });
      setUserModalOpen(false);
      setUserForm({ email: '', password: '', full_name: '', role: 'analyst' });
      setToastMessage({ text: 'Đã tạo tài khoản người dùng mới thành công.', type: 'success' });
      await loadUsers();
    } catch (err: unknown) {
      setModalError(err instanceof Error ? err.message : 'Không thể tạo tài khoản người dùng');
    } finally {
      setBusy(false);
    }
  };

  const handleRoleChange = async (userId: number, newRole: string) => {
    if (userId === currentUserId) return;
    setBusy(true);
    try {
      await updateUserRoleApi(userId, newRole);
      setToastMessage({
        text: `Đã cập nhật vai trò thành "${getRoleLabel(newRole)}" thành công.`,
        type: 'success',
      });
      await loadUsers();
    } catch (err: unknown) {
      setToastMessage({
        text: err instanceof Error ? err.message : 'Không thể đổi vai trò người dùng',
        type: 'error',
      });
    } finally {
      setBusy(false);
    }
  };

  const handleToggleStatus = async (userId: number, email: string, isCurrentlyDisabled: boolean) => {
    if (userId === currentUserId) return;
    if (!isCurrentlyDisabled) {
      const ok = confirm(`Bạn có chắc chắn muốn khóa tài khoản "${email}"? Người dùng này sẽ không thể đăng nhập.`);
      if (!ok) return;
    }

    setBusy(true);
    try {
      const res = await toggleUserStatusApi(userId);
      setToastMessage({
        text: res.message || (isCurrentlyDisabled ? 'Đã mở khóa tài khoản thành công.' : 'Đã khóa tài khoản thành công.'),
        type: 'success',
      });
      await loadUsers();
    } catch (err: unknown) {
      setToastMessage({
        text: err instanceof Error ? err.message : 'Không thể thay đổi trạng thái tài khoản',
        type: 'error',
      });
    } finally {
      setBusy(false);
    }
  };

  const userGridRows = useMemo(() => {
    return users
      .filter((u) => {
        const baseRole = u.role.replace('_disabled', '');
        return roleFilter === 'ALL' || baseRole === roleFilter;
      })
      .map((u) => {
        const isDisabled = u.isActive === false || u.role.includes('_disabled');
        const baseRole = u.role.replace('_disabled', '');
        return {
          id: u.id,
          fullName: u.fullName,
          email: u.email,
          createdAt: u.createdAt,
          baseRole,
          roleLabel: getRoleLabel(baseRole),
          isDisabled,
          statusLabel: isDisabled ? 'Đã khóa' : 'Hoạt động',
        };
      });
  }, [users, roleFilter]);

  return (
    <div className="space-y-5 font-sans">
      {/* Compact 1-Line Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-[#E5E7EB]">
        <h1 className="text-lg sm:text-xl font-bold text-[#1E293B] tracking-tight">
          Quản lý Tài khoản
        </h1>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => void loadUsers()}
            disabled={loading}
            className="px-3 py-1.5 rounded-lg bg-white hover:bg-[#F8FAF9] text-[#334155] hover:text-[#1E293B] border border-[#E5E7EB] text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Làm mới</span>
          </button>

          <button
            type="button"
            onClick={() => {
              setModalError('');
              setUserModalOpen(true);
            }}
            className="px-3 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Tạo người dùng mới</span>
          </button>
        </div>
      </div>

      {/* Toast message */}
      {toastMessage && (
        <div
          role={toastMessage.type === 'error' ? 'alert' : 'status'}
          className={`p-3 rounded-lg text-xs font-medium flex items-center justify-between border ${
            toastMessage.type === 'success'
              ? 'bg-[#F0F7F4] text-[#15803D] border-[#15803D]/25'
              : 'bg-red-50 text-[#DC2626] border-red-200'
          }`}
        >
          <div className="flex items-center gap-2">
            {toastMessage.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 shrink-0" />
            )}
            <span>{toastMessage.text}</span>
          </div>
          <button
            type="button"
            onClick={() => setToastMessage(null)}
            className="text-[#64748B] hover:text-[#1E293B] font-bold px-1 cursor-pointer"
          >
            ✕
          </button>
        </div>
      )}

      {/* Syncfusion Enterprise DataGrid: Users Table */}
      <section className="bg-white rounded-xl border border-[#E5E7EB] overflow-hidden">
        <div className="px-4 py-3 bg-[#F8FAF9] border-b border-[#E5E7EB] flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-[14px] font-bold text-[#1E293B]">
              Danh sách tài khoản ({userGridRows.length})
            </h2>
            <p className="text-[11.5px] text-[#64748B]">
              Phân quyền Quản trị viên (Admin), Chuyên viên phân tích (Analyst), Người dùng (User)
            </p>
          </div>

          <select
            aria-label="Lọc theo vai trò"
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="bg-white border border-[#E5E7EB] text-[#1E293B] px-2.5 py-1.5 rounded-lg text-xs font-medium focus:outline-none focus:border-[#2F6F4E]"
          >
            <option value="ALL">Tất cả vai trò ({users.length})</option>
            {ROLE_OPTIONS.map((r) => (
              <option key={r.value} value={r.value}>
                {r.label}
              </option>
            ))}
          </select>
        </div>

        <div className="p-4">
          <AgroGrid
            fileName="danh-sach-nguoi-dung-agroforecast"
            pageSize={15}
            height={430}
            data={userGridRows}
            columns={[
              { field: 'id', headerText: 'ID', kind: 'number', width: 75 },
              {
                field: 'fullName',
                headerText: 'Họ và tên',
                kind: 'text',
                width: 190,
                template: (row: Record<string, unknown>) => (
                  <span className="font-semibold text-[#1E293B]">{String(row.fullName ?? '')}</span>
                ),
              },
              { field: 'email', headerText: 'Email đăng nhập', kind: 'text', width: 230 },
              { field: 'createdAt', headerText: 'Ngày tạo', kind: 'date', width: 125 },
              {
                field: 'roleLabel',
                headerText: 'Vai trò',
                kind: 'text',
                width: 235,
                template: (row: Record<string, unknown>) => {
                  const id = Number(row.id);
                  const email = String(row.email ?? '');
                  const baseRole = String(row.baseRole ?? 'user');
                  const isSelf = id === currentUserId;
                  return (
                    <select
                      aria-label={`Đổi vai trò ${email}`}
                      disabled={busy || isSelf}
                      title={isSelf ? 'Không thể tự đổi vai trò tài khoản đang đăng nhập' : 'Đổi vai trò'}
                      value={baseRole}
                      onChange={(e) => void handleRoleChange(id, e.target.value)}
                      className="bg-white border border-[#E5E7EB] text-xs text-[#1E293B] rounded-md px-2 py-1 focus:outline-none focus:border-[#2F6F4E] disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {ROLE_OPTIONS.map((r) => (
                        <option key={r.value} value={r.value}>
                          {r.label}
                        </option>
                      ))}
                    </select>
                  );
                },
              },
              {
                field: 'statusLabel',
                headerText: 'Trạng thái',
                kind: 'text',
                align: 'Center',
                width: 115,
                template: (row: Record<string, unknown>) => {
                  const isDisabled = Boolean(row.isDisabled);
                  return isDisabled ? (
                    <span className="px-2 py-0.5 rounded-md bg-[#DC2626]/10 text-[#DC2626] text-[11px] font-semibold">
                      Đã khóa
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded-md bg-[#15803D]/10 text-[#15803D] text-[11px] font-semibold">
                      Hoạt động
                    </span>
                  );
                },
              },
              {
                field: 'actions',
                headerText: 'Thao tác',
                kind: 'text',
                align: 'Right',
                width: 100,
                allowSorting: false,
                allowFiltering: false,
                allowSearching: false,
                exportable: false,
                template: (row: Record<string, unknown>) => {
                  const id = Number(row.id);
                  const email = String(row.email ?? '');
                  const isDisabled = Boolean(row.isDisabled);
                  const isSelf = id === currentUserId;
                  return (
                    <button
                      type="button"
                      disabled={busy || isSelf}
                      onClick={() => void handleToggleStatus(id, email, isDisabled)}
                      className={`p-1.5 rounded-md text-xs transition-colors disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer ${
                        isDisabled
                          ? 'text-[#15803D] hover:bg-[#F0F7F4]'
                          : 'text-[#DC2626] hover:bg-red-50'
                      }`}
                      title={
                        isSelf
                          ? 'Không thể tự khóa tài khoản đang đăng nhập'
                          : isDisabled
                            ? 'Mở khóa tài khoản'
                            : 'Khóa tài khoản'
                      }
                    >
                      {isDisabled ? <Unlock className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
                    </button>
                  );
                },
              },
            ] as AgroColumn[]}
          />
        </div>
      </section>

      {/* Modal: Tạo Người Dùng Mới */}
      {userModalOpen && (
        <div className="fixed inset-0 z-50 bg-[#0F172A]/40 flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-white border border-[#E5E7EB] rounded-xl p-5 space-y-4 shadow-lg">
            <div className="flex items-center justify-between border-b border-[#E5E7EB] pb-2.5">
              <h3 className="text-base font-bold text-[#1E293B]">
                Tạo tài khoản người dùng mới
              </h3>
              <button
                type="button"
                onClick={() => setUserModalOpen(false)}
                className="text-[#64748B] hover:text-[#1E293B] font-bold text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            {modalError && (
              <p role="alert" className="text-xs text-[#DC2626] bg-red-50 border border-red-200 rounded-lg px-3 py-2 font-medium">
                {modalError}
              </p>
            )}

            <form onSubmit={handleCreateUser} className="space-y-3 text-xs">
              <div>
                <label className="block text-[#475569] font-semibold mb-1">Họ và tên</label>
                <input
                  type="text"
                  value={userForm.full_name}
                  onChange={(e) => setUserForm({ ...userForm, full_name: e.target.value })}
                  placeholder="VD: Nguyễn Văn A"
                  className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B]"
                  required
                />
              </div>

              <div>
                <label className="block text-[#475569] font-semibold mb-1">Email đăng nhập</label>
                <input
                  type="email"
                  value={userForm.email}
                  onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                  placeholder="VD: analyst@agroforecast.vn"
                  className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B]"
                  required
                />
              </div>

              <div>
                <label className="block text-[#475569] font-semibold mb-1">Mật khẩu (tối thiểu 6 ký tự)</label>
                <input
                  type="password"
                  minLength={6}
                  value={userForm.password}
                  onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
                  placeholder="Tối thiểu 6 ký tự"
                  className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B]"
                  required
                />
              </div>

              <div>
                <label className="block text-[#475569] font-semibold mb-1">Vai trò</label>
                <select
                  value={userForm.role}
                  onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}
                  className="w-full bg-white border border-[#E5E7EB] rounded-lg px-3 py-2 text-[#1E293B]"
                >
                  {ROLE_OPTIONS.map((r) => (
                    <option key={r.value} value={r.value}>
                      {r.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-[#E5E7EB]">
                <button
                  type="button"
                  onClick={() => setUserModalOpen(false)}
                  className="px-3.5 py-1.5 rounded-lg bg-white border border-[#E5E7EB] text-[#475569] font-semibold hover:bg-[#F8FAF9] cursor-pointer"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  disabled={busy}
                  className="px-4 py-1.5 rounded-lg bg-[#2F6F4E] hover:bg-[#24583D] text-white font-semibold disabled:opacity-50 cursor-pointer"
                >
                  {busy ? 'Đang tạo...' : 'Tạo người dùng'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
