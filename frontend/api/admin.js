const API_BASE_URL = "http://127.0.0.1:9999";


/* =========================================================
   AUTH
   ========================================================= */

function getStorage() {
    if (localStorage.getItem("auth_token")) {
        return localStorage;
    }

    return sessionStorage;
}


function getUser() {
    const storage = getStorage();

    return {
        token: storage.getItem("auth_token"),
        fullName: storage.getItem("full_name") || "",
        username: storage.getItem("username") || ""
    };
}


/* =========================================================
   API
   ========================================================= */

async function apiFetch(url, options = {}) {
    const user = getUser();

    const headers = {
        "Accept": "application/json",
        ...(options.headers || {})
    };

    if (user.token) {
        headers["Authorization"] = `Bearer ${user.token}`;
    }

    return fetch(url, {
        ...options,
        headers
    });
}


/* =========================================================
   LOGOUT
   ========================================================= */

function logout() {
    localStorage.clear();
    sessionStorage.clear();

    document.cookie.split(";").forEach((cookie) => {
        document.cookie = cookie
            .replace(/^ +/, "")
            .replace(
                /=.*/,
                "=;expires=" + new Date().toUTCString() + ";path=/"
            );
    });

    window.location.href = "../auth.html";
}


/* =========================================================
   HELPERS
   ========================================================= */

function money(value) {
    return Number(value || 0).toLocaleString("vi-VN") + " ₫";
}


function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function statusText(status) {
    const statusMap = {
        pending: "Chờ xử lý",
        confirmed: "Đã xác nhận",
        completed: "Hoàn thành",
        cancelled: "Đã huỷ",
        approved: "Đã duyệt",
        rejected: "Từ chối",
        resolved: "Đã xử lý",
        open: "Đang mở",
        active: "Đang hoạt động",
        inactive: "Không hoạt động"
    };

    const key = String(status || "").toLowerCase();

    return statusMap[key] || status || "Không xác định";
}


/* =========================================================
   RENDER ADMIN NAME
   ========================================================= */

function renderAdminName() {
    const user = getUser();

    const name =
        user.fullName ||
        user.username ||
        "Admin";

    const adminName =
        document.getElementById("adminName");

    const welcomeAdminName =
        document.getElementById("welcomeAdminName");

    if (adminName) {
        adminName.textContent = name;
    }

    if (welcomeAdminName) {
        welcomeAdminName.textContent = name;
    }
}


/* =========================================================
   LOAD DASHBOARD STATS
   ========================================================= */

async function loadDashboardStats() {
    const response = await apiFetch(
        `${API_BASE_URL}/admin/dashboard`
    );

    if (!response.ok) {
        throw new Error(
            `Dashboard API error: ${response.status}`
        );
    }

    const data = await response.json();

    const totalUsers =
        document.getElementById("totalUsers");

    const totalProviders =
        document.getElementById("totalProviders");

    const pendingProviders =
        document.getElementById("pendingProviders");

    const totalBookings =
        document.getElementById("totalBookings");

    if (totalUsers) {
        totalUsers.textContent =
            Number(
                data.total_users || 0
            ).toLocaleString("vi-VN");
    }

    if (totalProviders) {
        totalProviders.textContent =
            Number(
                data.total_providers || 0
            ).toLocaleString("vi-VN");
    }

    if (pendingProviders) {
        pendingProviders.textContent =
            `${Number(
                data.pending_providers || 0
            ).toLocaleString("vi-VN")} đang chờ duyệt`;
    }

    if (totalBookings) {
        totalBookings.textContent =
            Number(
                data.total_bookings || 0
            ).toLocaleString("vi-VN");
    }

    if (totalRevenue) {
        totalRevenue.textContent =
            money(data.total_revenue);
    }
}


/* =========================================================
   LOAD PROVIDERS
   ========================================================= */

async function loadPendingProviders() {
    const container =
        document.getElementById("pendingProvidersList");

    if (!container) {
        return;
    }

    try {
        const response = await apiFetch(
            `${API_BASE_URL}/service-providers/`
        );

        if (!response.ok) {
            throw new Error(
                `Provider API error: ${response.status}`
            );
        }

        const data = await response.json();

        const providers =
            Array.isArray(data)
                ? data
                : data.data ||
                  data.providers ||
                  [];

        const pending =
            providers
                .filter((provider) => {
                    const status =
                        String(
                            provider.verification_status ||
                            provider.VerificationStatus ||
                            provider.status ||
                            ""
                        ).toLowerCase();

                    return status === "pending";
                })
                .slice(0, 5);

        if (pending.length === 0) {
            container.innerHTML = `
                <div class="admin-empty">
                    Không có provider nào đang chờ duyệt.
                </div>
            `;

            return;
        }

        container.innerHTML =
            pending
                .map((provider) => {
                    const providerId =
                        provider.provider_id ??
                        provider.ProviderID ??
                        provider.id ??
                        "";

                    const businessName =
                        provider.business_name ??
                        provider.BusinessName ??
                        "Provider";

                    const address =
                        provider.business_address ??
                        provider.BusinessAddress ??
                        "Chưa cập nhật địa chỉ";

                    const status =
                        provider.verification_status ??
                        provider.VerificationStatus ??
                        provider.status ??
                        "pending";

                    return `
                        <div class="admin-list-item">

                            <div class="admin-list-main">

                                <p class="admin-list-title">
                                    ${escapeHtml(businessName)}
                                </p>

                                <p class="admin-list-description">
                                    ID: ${escapeHtml(providerId)}
                                    · ${escapeHtml(address)}
                                </p>

                            </div>

                            <div class="admin-list-action">

                                <span class="admin-status">
                                    ${escapeHtml(
                                        statusText(status)
                                    )}
                                </span>

                            </div>

                        </div>
                    `;
                })
                .join("");

    } catch (error) {
        console.error(
            "Cannot load pending providers:",
            error
        );

        container.innerHTML = `
            <div class="admin-empty">
                Không thể tải danh sách provider.
            </div>
        `;
    }
}


/* =========================================================
   LOAD COMPLAINTS
   ========================================================= */

async function loadComplaints() {
    const container =
        document.getElementById("complaintsList");

    if (!container) {
        return;
    }

    try {
        const response = await apiFetch(
            `${API_BASE_URL}/complaints/`
        );

        if (!response.ok) {
            throw new Error(
                `Complaint API error: ${response.status}`
            );
        }

        const data = await response.json();

        const complaints =
            Array.isArray(data)
                ? data
                : data.data ||
                  data.complaints ||
                  [];

        const recentComplaints =
            complaints.slice(0, 5);

        if (recentComplaints.length === 0) {
            container.innerHTML = `
                <div class="admin-empty">
                    Chưa có khiếu nại nào.
                </div>
            `;

            return;
        }

        container.innerHTML =
            recentComplaints
                .map((complaint) => {
                    const complaintId =
                        complaint.complaint_id ??
                        complaint.ComplaintID ??
                        complaint.id ??
                        "";

                    const description =
                        complaint.description ??
                        complaint.Description ??
                        "Không có nội dung";

                    const status =
                        complaint.status ??
                        complaint.Status ??
                        "open";

                    return `
                        <div class="admin-list-item">

                            <div class="admin-list-main">

                                <p class="admin-list-title">
                                    Khiếu nại #${escapeHtml(
                                        complaintId
                                    )}
                                </p>

                                <p class="admin-list-description">
                                    ${escapeHtml(description)}
                                </p>

                            </div>

                            <div class="admin-list-action">

                                <span class="admin-status">
                                    ${escapeHtml(
                                        statusText(status)
                                    )}
                                </span>

                            </div>

                        </div>
                    `;
                })
                .join("");

    } catch (error) {
        console.error(
            "Cannot load complaints:",
            error
        );

        container.innerHTML = `
            <div class="admin-empty">
                Không thể tải danh sách khiếu nại.
            </div>
        `;
    }
}


/* =========================================================
   LOAD RECENT BOOKINGS
   ========================================================= */

async function loadRecentBookings() {
    const container =
        document.getElementById("recentBookings");

    if (!container) {
        return;
    }

    try {
        const response = await apiFetch(
            `${API_BASE_URL}/bookings/`
        );

        if (!response.ok) {
            throw new Error(
                `Booking API error: ${response.status}`
            );
        }

        const data = await response.json();

        const bookings =
            Array.isArray(data)
                ? data
                : data.data ||
                  data.bookings ||
                  [];

        const recentBookings =
            bookings.slice(0, 8);

        if (recentBookings.length === 0) {
            container.innerHTML = `
                <tr>
                    <td
                        colspan="6"
                        class="admin-table-empty"
                    >
                        Chưa có booking nào.
                    </td>
                </tr>
            `;

            return;
        }

        container.innerHTML =
            recentBookings
                .map((booking) => {
                    const bookingId =
                        booking.booking_id ??
                        booking.BookingID ??
                        booking.id ??
                        "";

                    const photographerId =
                        booking.photographer_id ??
                        booking.PhotographerID ??
                        "";

                    const spaceId =
                        booking.space_id ??
                        booking.SpaceID ??
                        "";

                    const startTime =
                        booking.start_time ??
                        booking.StartTime ??
                        "";

                    const endTime =
                        booking.end_time ??
                        booking.EndTime ??
                        "";

                    const status =
                        booking.status ??
                        booking.Status ??
                        "";

                    const totalPrice =
                        booking.total_price ??
                        booking.TotalPrice ??
                        0;

                    return `
                        <tr>

                            <td>
                                #${escapeHtml(bookingId)}
                            </td>

                            <td>
                                ${escapeHtml(
                                    photographerId
                                )}
                            </td>

                            <td>
                                ${escapeHtml(
                                    spaceId
                                )}
                            </td>

                            <td>
                                ${escapeHtml(startTime)}
                                <br>
                                ${escapeHtml(endTime)}
                            </td>

                            <td>
                                <span class="admin-status">
                                    ${escapeHtml(
                                        statusText(status)
                                    )}
                                </span>
                            </td>

                            <td>
                                ${escapeHtml(
                                    money(totalPrice)
                                )}
                            </td>

                        </tr>
                    `;
                })
                .join("");

    } catch (error) {
        console.error(
            "Cannot load bookings:",
            error
        );

        container.innerHTML = `
            <tr>
                <td
                    colspan="6"
                    class="admin-table-empty"
                >
                    Không thể tải danh sách booking.
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   LOAD PAYMENTS
   ========================================================= */

async function loadPayments() {
    const tableBody =
        document.getElementById(
            "paymentsTableBody"
        );

    if (!tableBody) {
        return;
    }

    try {
        const response =
            await apiFetch(
                `${API_BASE_URL}/payments/`
            );

        if (!response.ok) {
            throw new Error(
                `Payment API error: ${response.status}`
            );
        }

        const data =
            await response.json();

        const payments =
            Array.isArray(data)
                ? data
                : data.data ||
                  data.payments ||
                  [];

        if (payments.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="7"
                        class="admin-table-empty"
                    >
                        Chưa có giao dịch nào.
                    </td>
                </tr>
            `;

            return;
        }

        tableBody.innerHTML =
            payments
                .map((payment) => {
                    const paymentId =
                        payment.id ??
                        payment.PaymentID ??
                        "";

                    const invoiceId =
                        payment.invoice_id ??
                        payment.InvoiceID ??
                        "";

                    const paymentMethod =
                        payment.payment_method ??
                        payment.PaymentMethod ??
                        "Không xác định";

                    const amount =
                        payment.amount ??
                        payment.Amount ??
                        0;

                    const status =
                        payment.status ??
                        payment.Status ??
                        "";

                    const createdAt =
                        payment.created_at ??
                        payment.CreatedAt ??
                        "";

                    const paidAt =
                        payment.paid_at ??
                        payment.PaidAt ??
                        "";

                    return `
                        <tr>

                            <td>
                                #${escapeHtml(paymentId)}
                            </td>

                            <td>
                                #${escapeHtml(invoiceId)}
                            </td>

                            <td>
                                ${escapeHtml(
                                    paymentMethod
                                )}
                            </td>

                            <td>
                                ${escapeHtml(
                                    money(amount)
                                )}
                            </td>

                            <td>
                                <span class="admin-status">
                                    ${escapeHtml(
                                        statusText(status)
                                    )}
                                </span>
                            </td>

                            <td>
                                ${escapeHtml(createdAt)}
                            </td>

                            <td>
                                ${
                                    paidAt
                                        ? escapeHtml(paidAt)
                                        : "Chưa thanh toán"
                                }
                            </td>

                        </tr>
                    `;
                })
                .join("");

    } catch (error) {
        console.error(
            "Cannot load payments:",
            error
        );

        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="7"
                    class="admin-table-empty"
                >
                    Không thể tải danh sách giao dịch.
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   LOAD DASHBOARD
   ========================================================= */

async function loadDashboard() {
    renderAdminName();

    try {
        await loadDashboardStats();
    } catch (error) {
        console.error(
            "Cannot load dashboard stats:",
            error
        );
    }

    await loadPendingProviders();
    await loadComplaints();
    await loadRecentBookings();
}


/* =========================================================
   ADMIN ACCOUNTS
   ========================================================= */

let adminUsers = [];
let adminProviders = [];
let selectedProviderId = null;


/* =========================================================
   LOAD ACCOUNTS
   ========================================================= */

async function loadAccounts() {
    const tableBody =
        document.getElementById(
            "accountsTableBody"
        );

    if (!tableBody) {
        return;
    }

    try {
        const [
            usersResponse,
            providersResponse
        ] = await Promise.all([
            apiFetch(
                `${API_BASE_URL}/admin/users`
            ),
            apiFetch(
                `${API_BASE_URL}/admin/providers`
            )
        ]);

        if (!usersResponse.ok) {
            throw new Error(
                `User API error: ${usersResponse.status}`
            );
        }

        if (!providersResponse.ok) {
            throw new Error(
                `Provider API error: ${providersResponse.status}`
            );
        }

        const usersData =
            await usersResponse.json();

        const providersData =
            await providersResponse.json();

        adminUsers =
            Array.isArray(usersData)
                ? usersData
                : usersData.data ||
                  usersData.users ||
                  [];

        adminProviders =
            Array.isArray(providersData)
                ? providersData
                : providersData.data ||
                  providersData.providers ||
                  [];

        renderAccounts();

    } catch (error) {
        console.error(
            "Cannot load accounts:",
            error
        );

        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="7"
                    class="admin-table-empty"
                >
                    Không thể tải danh sách người dùng.
                </td>
            </tr>
        `;
    }
}


/* =========================================================
   FIND PROVIDER
   ========================================================= */

function findProviderByUserId(userId) {
    return adminProviders.find(
        (provider) =>
            Number(provider.user_id) === Number(userId)
    );
}


/* =========================================================
   SHOW USER DETAIL
   ========================================================= */

function showUserDetail(userId) {
    const modal =
        document.getElementById(
            "providerModal"
        );

    const modalBody =
        document.getElementById(
            "providerModalBody"
        );

    const approveButton =
        document.getElementById(
            "approveProviderButton"
        );

    if (!modal || !modalBody) {
        return;
    }

    const user =
        adminUsers.find(
            (item) =>
                Number(item.user_id) === Number(userId)
        );

    if (!user) {
        return;
    }

    /*
     * Tìm Provider trực tiếp từ user hoặc
     * từ danh sách Provider.
     */
    const provider =
        user.provider ||
        findProviderByUserId(user.user_id);

    selectedProviderId =
        provider
            ? Number(provider.id)
            : null;

    let providerHtml = "";

    /*
     * Nếu tài khoản là Provider thì hiển thị
     * thêm thông tin doanh nghiệp.
     */
    if (provider) {
        providerHtml = `
            <hr>

            <h3>
                Thông tin Provider
            </h3>

            <div>
                <strong>
                    Tên doanh nghiệp
                </strong>

                <span>
                    ${escapeHtml(
                        provider.business_name ||
                        provider.BusinessName ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Mã số thuế
                </strong>

                <span>
                    ${escapeHtml(
                        provider.tax_code ||
                        provider.TaxCode ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Địa chỉ kinh doanh
                </strong>

                <span>
                    ${escapeHtml(
                        provider.business_address ||
                        provider.BusinessAddress ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Trạng thái Provider
                </strong>

                <span>
                    ${escapeHtml(
                        statusText(
                            provider.verification_status ||
                            provider.VerificationStatus
                        )
                    )}
                </span>
            </div>

            <div>
                <strong>
                    License
                </strong>

                <span>
                    ${
                        provider.license_url ||
                        provider.LicenseUrl
                            ? `
                                <a
                                    href="${escapeHtml(
                                        provider.license_url ||
                                        provider.LicenseUrl
                                    )}"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Xem tài liệu
                                </a>
                            `
                            : "Chưa cập nhật"
                    }
                </span>
            </div>
        `;
    }

    modalBody.innerHTML = `
        <div class="admin-provider-detail">

            <h3>
                Thông tin tài khoản
            </h3>

            <div>
                <strong>
                    User ID
                </strong>

                <span>
                    #${escapeHtml(user.user_id)}
                </span>
            </div>

            <div>
                <strong>
                    Username
                </strong>

                <span>
                    ${escapeHtml(
                        user.username ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Họ và tên
                </strong>

                <span>
                    ${escapeHtml(
                        user.full_name ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Email
                </strong>

                <span>
                    ${escapeHtml(
                        user.email ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Số điện thoại
                </strong>

                <span>
                    ${escapeHtml(
                        user.phone ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Giới tính
                </strong>

                <span>
                    ${escapeHtml(
                        user.gender ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Vai trò
                </strong>

                <span>
                    ${escapeHtml(
                        getRoleText(user)
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Trạng thái tài khoản
                </strong>

                <span>
                    ${escapeHtml(
                        statusText(user.status)
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Ngày tạo
                </strong>

                <span>
                    ${
                        user.created_at
                            ? escapeHtml(
                                user.created_at
                            )
                            : "Chưa cập nhật"
                    }
                </span>
            </div>

            ${providerHtml}

        </div>
    `;


    /*
     * CHỈ Provider pending mới có nút Duyệt.
     *
     * Người dùng / Photographer:
     * provider = null
     * => hidden = true
     *
     * Provider approved:
     * status = approved
     * => hidden = true
     *
     * Provider pending:
     * status = pending
     * => hidden = false
     */
    if (approveButton) {

        const providerStatus =
            provider
                ? (
                    provider.verification_status ||
                    provider.VerificationStatus ||
                    ""
                )
                : "";

        const isPendingProvider =
            Boolean(provider) &&
            String(providerStatus).toLowerCase() === "pending";

        approveButton.hidden =
            !isPendingProvider;

        approveButton.disabled = false;

        approveButton.textContent =
            "Duyệt Provider";
    }

    modal.hidden = false;
}


/* =========================================================
   ROLE TEXT
   ========================================================= */

function getRoleText(user) {
    const provider =
        user.provider ||
        findProviderByUserId(user.user_id);

    if (provider) {
        return "Provider";
    }

    return "Người dùng";
}


/* =========================================================
   RENDER ACCOUNTS
   ========================================================= */

function renderAccounts() {
    const tableBody =
        document.getElementById(
            "accountsTableBody"
        );

    if (!tableBody) {
        return;
    }

    if (adminUsers.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="7"
                    class="admin-table-empty"
                >
                    Chưa có người dùng nào.
                </td>
            </tr>
        `;

        return;
    }

    tableBody.innerHTML =
        adminUsers
            .map((user) => {

                /*
                 * Nếu user có provider object
                 * thì đây là Provider.
                 */
                const provider =
                    user.provider ||
                    findProviderByUserId(
                        user.user_id
                    );

                const role =
                    getRoleText(user);

                const status =
                    user.status ||
                    "unknown";

                const userId =
                    user.user_id ??
                    "";

                const fullName =
                    user.full_name ||
                    "Chưa cập nhật";

                const email =
                    user.email ||
                    "Chưa cập nhật";

                const phone =
                    user.phone ||
                    "Chưa cập nhật";


                /*
                 * Tất cả tài khoản đều có nút Xem.
                 */
                let actionHtml = `
                    <button
                        type="button"
                        class="admin-view-button"
                        onclick="showUserDetail(${Number(userId)})"
                    >
                        Xem
                    </button>
                `;


                /*
                 * CHỈ Provider pending mới có Duyệt.
                 */
                if (provider) {

                    const providerStatus =
                        provider.verification_status ||
                        provider.VerificationStatus ||
                        "unknown";

                    if (
                        String(providerStatus).toLowerCase()
                        === "pending"
                    ) {

                        actionHtml += `
                            <button
                                type="button"
                                class="admin-approve-button"
                                onclick="showProviderDetail(${Number(provider.id)})"
                            >
                                Duyệt
                            </button>
                        `;
                    }
                }


                return `
                    <tr>

                        <td>
                            #${escapeHtml(userId)}
                        </td>

                        <td>
                            ${escapeHtml(fullName)}
                        </td>

                        <td>
                            ${escapeHtml(email)}
                        </td>

                        <td>
                            ${escapeHtml(phone)}
                        </td>

                        <td>
                            ${escapeHtml(role)}
                        </td>

                        <td>
                            <span class="admin-status">
                                ${escapeHtml(
                                    statusText(status)
                                )}
                            </span>
                        </td>

                        <td>
                            <div class="admin-actions">
                                ${actionHtml}
                            </div>
                        </td>

                    </tr>
                `;
            })
            .join("");
}


/* =========================================================
   SHOW PROVIDER DETAIL
   ========================================================= */

function showProviderDetail(providerId) {
    const modal =
        document.getElementById(
            "providerModal"
        );

    const modalBody =
        document.getElementById(
            "providerModalBody"
        );

    const approveButton =
        document.getElementById(
            "approveProviderButton"
        );

    if (!modal || !modalBody) {
        return;
    }

    const provider =
        adminProviders.find(
            (item) =>
                Number(item.id) === Number(providerId)
        );

    if (!provider) {
        return;
    }

    selectedProviderId =
        Number(provider.id);

    const status =
        provider.verification_status ||
        provider.VerificationStatus ||
        "unknown";

    const licenseUrl =
        provider.license_url ||
        provider.LicenseUrl ||
        "";

    modalBody.innerHTML = `
        <div class="admin-provider-detail">

            <div>
                <strong>
                    Tên doanh nghiệp
                </strong>

                <span>
                    ${escapeHtml(
                        provider.business_name ||
                        provider.BusinessName ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Mã số thuế
                </strong>

                <span>
                    ${escapeHtml(
                        provider.tax_code ||
                        provider.TaxCode ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Địa chỉ
                </strong>

                <span>
                    ${escapeHtml(
                        provider.business_address ||
                        provider.BusinessAddress ||
                        "Chưa cập nhật"
                    )}
                </span>
            </div>

            <div>
                <strong>
                    Trạng thái xác minh
                </strong>

                <span class="admin-status">
                    ${escapeHtml(
                        statusText(status)
                    )}
                </span>
            </div>

            <div>
                <strong>
                    License
                </strong>

                <span>
                    ${
                        licenseUrl
                            ? `
                                <a
                                    href="${escapeHtml(
                                        licenseUrl
                                    )}"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Xem tài liệu
                                </a>
                            `
                            : "Chưa cập nhật"
                    }
                </span>
            </div>

            <div>
                <strong>
                    Ngày duyệt
                </strong>

                <span>
                    ${
                        provider.approved_at
                            ? escapeHtml(
                                provider.approved_at
                            )
                            : "Chưa duyệt"
                    }
                </span>
            </div>

        </div>
    `;


    /*
     * Trong modal Provider:
     * chỉ pending mới được duyệt.
     */
    if (approveButton) {

        const isPending =
            String(status).toLowerCase() === "pending";

        approveButton.hidden =
            !isPending;

        approveButton.disabled = false;

        approveButton.textContent =
            "Duyệt Provider";
    }

    modal.hidden = false;
}


/* =========================================================
   CLOSE PROVIDER MODAL
   ========================================================= */

function closeProviderModal() {
    const modal =
        document.getElementById(
            "providerModal"
        );

    const approveButton =
        document.getElementById(
            "approveProviderButton"
        );

    if (modal) {
        modal.hidden = true;
    }

    if (approveButton) {
        approveButton.hidden = true;
        approveButton.disabled = false;
        approveButton.textContent =
            "Duyệt Provider";
    }

    selectedProviderId = null;
}


/* =========================================================
   APPROVE PROVIDER
   ========================================================= */

async function approveProvider() {
    if (!selectedProviderId) {
        return;
    }

    const approveButton =
        document.getElementById(
            "approveProviderButton"
        );

    if (approveButton) {
        approveButton.disabled = true;
        approveButton.textContent =
            "Đang duyệt...";
    }

    try {
        const response =
            await apiFetch(
                `${API_BASE_URL}/admin/providers/${selectedProviderId}/approve`,
                {
                    method: "PUT"
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                `Approve API error: ${response.status}`
            );
        }

        alert(
            "Duyệt Provider thành công."
        );

        closeProviderModal();

        await loadAccounts();

    } catch (error) {

        console.error(
            "Cannot approve provider:",
            error
        );

        alert(
            error.message ||
            "Không thể duyệt Provider."
        );

        if (approveButton) {
            approveButton.disabled = false;
            approveButton.textContent =
                "Duyệt Provider";
        }
    }
}


/* =========================================================
   ADMIN SETTINGS
   ========================================================= */

async function loadAdminSettings() {

    const fullNameInput =
        document.getElementById(
            "adminFullName"
        );

    const emailInput =
        document.getElementById(
            "adminEmail"
        );

    const usernameInput =
        document.getElementById(
            "adminUsername"
        );

    if (
        !fullNameInput ||
        !emailInput ||
        !usernameInput
    ) {
        return;
    }

    const storage =
        getStorage();

    const token =
        storage.getItem("auth_token");

    const userId =
        storage.getItem("user_id");

    if (!token || !userId) {
        window.location.href =
            "../auth.html";

        return;
    }

    try {

        const response =
            await apiFetch(
                `${API_BASE_URL}/users/${userId}`
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                "Không thể tải thông tin Admin."
            );
        }

        fullNameInput.value =
            data.full_name || "";

        emailInput.value =
            data.email || "";

        usernameInput.value =
            data.username || "";

    } catch (error) {

        console.error(
            "LOAD ADMIN SETTINGS ERROR:",
            error
        );

        showAdminSettingsMessage(
            "Không thể tải thông tin tài khoản.",
            "error"
        );
    }
}


/* =========================================================
   SAVE ADMIN SETTINGS
   ========================================================= */

async function saveAdminSettings(event) {

    event.preventDefault();

    const fullNameInput =
        document.getElementById(
            "adminFullName"
        );

    const emailInput =
        document.getElementById(
            "adminEmail"
        );

    const saveButton =
        document.querySelector(
            ".admin-settings-save"
        );

    const storage =
        getStorage();

    const token =
        storage.getItem("auth_token");

    const userId =
        storage.getItem("user_id");

    if (!token || !userId) {

        window.location.href =
            "../auth.html";

        return;
    }

    const fullName =
        fullNameInput.value.trim();

    const email =
        emailInput.value.trim();

    if (!fullName || !email) {

        showAdminSettingsMessage(
            "Vui lòng nhập đầy đủ thông tin.",
            "error"
        );

        return;
    }

    if (saveButton) {

        saveButton.disabled = true;

        saveButton.textContent =
            "Đang lưu...";
    }

    try {

        const response =
            await apiFetch(
                `${API_BASE_URL}/users/${userId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        full_name:
                            fullName,

                        email:
                            email
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Cập nhật thông tin thất bại."
            );
        }


        /* =========================
           UPDATE STORAGE
           ========================= */

        storage.setItem(
            "full_name",
            data.full_name ||
            fullName
        );

        storage.setItem(
            "email",
            data.email ||
            email
        );


        /* =========================
           UPDATE NAVBAR
           ========================= */

        const navAdminName =
            document.getElementById(
                "navAdminName"
            );

        if (navAdminName) {

            navAdminName.textContent =
                data.full_name ||
                fullName;
        }


        const adminName =
            document.getElementById(
                "adminName"
            );

        if (adminName) {

            adminName.textContent =
                data.full_name ||
                fullName;
        }


        showAdminSettingsMessage(
            "Đã cập nhật thông tin Admin thành công.",
            "success"
        );

    } catch (error) {

        console.error(
            "SAVE ADMIN SETTINGS ERROR:",
            error
        );

        showAdminSettingsMessage(
            error.message ||
            "Không thể cập nhật thông tin.",
            "error"
        );

    } finally {

        if (saveButton) {

            saveButton.disabled = false;

            saveButton.textContent =
                "Lưu thay đổi";
        }
    }
}


/* =========================================================
   SETTINGS MESSAGE
   ========================================================= */

function showAdminSettingsMessage(
    message,
    type = "success"
) {
    const messageBox =
        document.getElementById(
            "adminSettingsMessage"
        );

    if (!messageBox) {
        return;
    }

    messageBox.textContent =
        message;

    messageBox.className =
        `admin-settings-message ${type}`;
}


/* =========================================================
   SETTINGS INIT
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "adminSettingsForm"
            );

        if (form) {

            form.addEventListener(
                "submit",
                saveAdminSettings
            );

            loadAdminSettings();
        }
    }
);


/* =========================================================
   INIT
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {
        loadDashboard();
        loadAccounts();
    }
);