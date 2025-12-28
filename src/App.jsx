import React, { useState, useEffect } from 'react';
import { ShoppingCart, Search, User, LogOut, Trash2, Plus, Minus } from 'lucide-react';

// Mock Backend Service (Giả lập API)
const mockBackend = {
  users: JSON.parse(localStorage.getItem('users') || '[]'),
  products: [
    { id: 1, name: 'Quạt Trần KDK K15Z', price: 1200000, brand: 'KDK', image: 'https://images.unsplash.com/photo-1632225896174-4ac5c5c6d36b?w=300', description: 'Quạt trần cao cấp, tiết kiệm điện' },
    { id: 2, name: 'Quạt Đứng Panasonic F-409', price: 850000, brand: 'Panasonic', image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300', description: 'Quạt đứng 5 cánh, điều khiển từ xa' },
    { id: 3, name: 'Quạt Hộp Senko B113', price: 450000, brand: 'Senko', image: 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=300', description: 'Quạt hộp công nghiệp, gió mạnh' },
    { id: 4, name: 'Quạt Điều Hòa Sunhouse SHD7730', price: 2500000, brand: 'Sunhouse', image: 'https://images.unsplash.com/photo-1597452485669-2c7bb5fef90d?w=300', description: 'Quạt điều hòa, làm mát hiệu quả' },
    { id: 5, name: 'Quạt Bàn Toshiba F-LSA10', price: 350000, brand: 'Toshiba', image: 'https://images.unsplash.com/photo-1583523032343-bacc5b6f1f5f?w=300', description: 'Quạt bàn mini, tiện lợi' },
    { id: 6, name: 'Quạt Treo Tường Mitsubishi CY-10WH', price: 680000, brand: 'Mitsubishi', image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300', description: 'Quạt treo tường, điều chỉnh linh hoạt' }
  ],
  carts: JSON.parse(localStorage.getItem('carts') || '{}'),
  
  saveUsers() {
    localStorage.setItem('users', JSON.stringify(this.users));
  },
  
  saveCarts() {
    localStorage.setItem('carts', JSON.stringify(this.carts));
  },
  
  // Validate password (8-16 ký tự)
  validatePassword(password) {
    // Kiểm tra độ dài
    if (password.length < 8 || password.length > 16) {
      return { valid: false, message: 'Mật khẩu phải từ 8 đến 16 ký tự!' };
    }
    
    // Kiểm tra có chữ hoa
    if (!/[A-Z]/.test(password)) {
      return { valid: false, message: 'Mật khẩu phải có ít nhất 1 chữ IN HOA!' };
    }
    
    // Kiểm tra có chữ thường
    if (!/[a-z]/.test(password)) {
      return { valid: false, message: 'Mật khẩu phải có ít nhất 1 chữ thường!' };
    }
    
    // Kiểm tra có ký tự đặc biệt
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return { valid: false, message: 'Mật khẩu phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*...)!' };
    }
    
    return { valid: true };
  },
  
  // Mã hóa mật khẩu đơn giản (trong thực tế dùng bcrypt)
  hashPassword(password) {
    return btoa(password + 'salt123'); // Base64 encode
  },
  
  verifyPassword(password, hash) {
    return this.hashPassword(password) === hash;
  },
  
  // API Methods
  register(username, email, password) {
    const validation = this.validatePassword(password);
    if (!validation.valid) {
      return { success: false, message: validation.message };
    }
    
    if (this.users.find(u => u.email === email)) {
      return { success: false, message: 'Email đã được sử dụng!' };
    }
    
    const user = {
      id: Date.now(),
      username,
      email,
      password: this.hashPassword(password),
      createdAt: new Date().toISOString()
    };
    
    this.users.push(user);
    this.saveUsers();
    this.carts[user.id] = [];
    this.saveCarts();
    
    return { success: true, user: { id: user.id, username, email } };
  },
  
  login(email, password) {
    const user = this.users.find(u => u.email === email);
    
    if (!user) {
      return { success: false, message: 'Email hoặc mật khẩu không đúng!' };
    }
    
    if (!this.verifyPassword(password, user.password)) {
      return { success: false, message: 'Email hoặc mật khẩu không đúng!' };
    }
    
    return { 
      success: true, 
      user: { id: user.id, username: user.username, email: user.email },
      token: btoa(`${user.id}:${Date.now()}`) // Mock JWT
    };
  },
  
  getProducts(search = '', brand = '', minPrice = 0, maxPrice = Infinity) {
    return this.products.filter(p => {
      const matchName = p.name.toLowerCase().includes(search.toLowerCase());
      const matchBrand = !brand || p.brand === brand;
      const matchPrice = p.price >= minPrice && p.price <= maxPrice;
      return matchName && matchBrand && matchPrice;
    });
  },
  
  getCart(userId) {
    return this.carts[userId] || [];
  },
  
  addToCart(userId, productId, quantity = 1) {
    if (!this.carts[userId]) this.carts[userId] = [];
    
    const existing = this.carts[userId].find(item => item.productId === productId);
    if (existing) {
      existing.quantity += quantity;
    } else {
      this.carts[userId].push({ productId, quantity });
    }
    
    this.saveCarts();
    return { success: true };
  },
  
  updateCartItem(userId, productId, quantity) {
    const item = this.carts[userId]?.find(item => item.productId === productId);
    if (item) {
      item.quantity = quantity;
      this.saveCarts();
    }
    return { success: true };
  },
  
  removeFromCart(userId, productId) {
    if (this.carts[userId]) {
      this.carts[userId] = this.carts[userId].filter(item => item.productId !== productId);
      this.saveCarts();
    }
    return { success: true };
  }
};

// Main App Component
function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('home');
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBrand, setSelectedBrand] = useState('');
  const [priceRange, setPriceRange] = useState({ min: 0, max: 10000000 });
  
  // Auth states
  const [authMode, setAuthMode] = useState('login');
  const [authForm, setAuthForm] = useState({ username: '', email: '', password: '' });
  const [authError, setAuthError] = useState('');

  // Load user from session
  useEffect(() => {
    const savedUser = sessionStorage.getItem('currentUser');
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    }
  }, []);

  // Load products
  useEffect(() => {
    setProducts(mockBackend.getProducts(searchQuery, selectedBrand, priceRange.min, priceRange.max));
  }, [searchQuery, selectedBrand, priceRange]);

  // Load cart
  useEffect(() => {
    if (currentUser) {
      setCart(mockBackend.getCart(currentUser.id));
    }
  }, [currentUser]);

  // Validate password frontend (8-16 ký tự, có chữ hoa, chữ thường, ký tự đặc biệt)
  const validatePassword = (password) => {
    if (password.length < 8) return 'Mật khẩu phải có ít nhất 8 ký tự!';
    if (password.length > 16) return 'Mật khẩu không được quá 16 ký tự!';
    
    // Kiểm tra có chữ hoa
    if (!/[A-Z]/.test(password)) {
      return 'Mật khẩu phải có ít nhất 1 chữ IN HOA!';
    }
    
    // Kiểm tra có chữ thường
    if (!/[a-z]/.test(password)) {
      return 'Mật khẩu phải có ít nhất 1 chữ thường!';
    }
    
    // Kiểm tra có ký tự đặc biệt
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return 'Mật khẩu phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*...)!';
    }
    
    return '';
  };

  // Handle auth
  const handleAuth = () => {
    setAuthError('');

    // Validate password
    const pwdError = validatePassword(authForm.password);
    if (pwdError) {
      setAuthError(pwdError);
      return;
    }

    if (authMode === 'register') {
      const result = mockBackend.register(authForm.username, authForm.email, authForm.password);
      if (result.success) {
        setCurrentUser(result.user);
        sessionStorage.setItem('currentUser', JSON.stringify(result.user));
        setCurrentPage('home');
        setAuthForm({ username: '', email: '', password: '' });
      } else {
        setAuthError(result.message);
      }
    } else {
      const result = mockBackend.login(authForm.email, authForm.password);
      if (result.success) {
        setCurrentUser(result.user);
        sessionStorage.setItem('currentUser', JSON.stringify(result.user));
        setCurrentPage('home');
        setAuthForm({ username: '', email: '', password: '' });
      } else {
        setAuthError(result.message);
      }
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    sessionStorage.removeItem('currentUser');
    setCart([]);
    setCurrentPage('home');
  };

  const handleAddToCart = (productId) => {
    if (!currentUser) {
      setCurrentPage('auth');
      return;
    }
    mockBackend.addToCart(currentUser.id, productId);
    setCart(mockBackend.getCart(currentUser.id));
  };

  const handleUpdateCart = (productId, quantity) => {
    if (quantity <= 0) {
      mockBackend.removeFromCart(currentUser.id, productId);
    } else {
      mockBackend.updateCartItem(currentUser.id, productId, quantity);
    }
    setCart(mockBackend.getCart(currentUser.id));
  };

  const handleRemoveFromCart = (productId) => {
    mockBackend.removeFromCart(currentUser.id, productId);
    setCart(mockBackend.getCart(currentUser.id));
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => {
      const product = products.find(p => p.id === item.productId);
      return total + (product ? product.price * item.quantity : 0);
    }, 0);
  };

  const brands = [...new Set(mockBackend.products.map(p => p.brand))];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 
              className="text-2xl font-bold cursor-pointer hover:text-blue-100"
              onClick={() => setCurrentPage('home')}
            >
              🌀 Cửa Hàng Quạt Điện
            </h1>
            
            <div className="flex items-center gap-4">
              {currentUser ? (
                <>
                  <button
                    onClick={() => setCurrentPage('cart')}
                    className="relative p-2 hover:bg-blue-700 rounded-lg transition"
                  >
                    <ShoppingCart size={24} />
                    {cart.length > 0 && (
                      <span className="absolute -top-1 -right-1 bg-red-500 text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {cart.length}
                      </span>
                    )}
                  </button>
                  <div className="flex items-center gap-2">
                    <User size={20} />
                    <span className="text-sm">{currentUser.username}</span>
                    <button
                      onClick={handleLogout}
                      className="p-2 hover:bg-blue-700 rounded-lg transition"
                    >
                      <LogOut size={20} />
                    </button>
                  </div>
                </>
              ) : (
                <button
                  onClick={() => setCurrentPage('auth')}
                  className="bg-white text-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-50 transition"
                >
                  Đăng nhập
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-4 py-8">
        {currentPage === 'auth' && (
          <div className="flex items-center justify-center" style={{ minHeight: 'calc(100vh - 96px)' }}>
            <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
                {authMode === 'login' ? 'Đăng Nhập' : 'Đăng Ký'}
              </h2>
            
            <div className="space-y-4">
              {authMode === 'register' && (
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Tên người dùng</label>
                  <input
                    type="text"
                    required
                    value={authForm.username}
                    onChange={(e) => setAuthForm({...authForm, username: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                    placeholder="Nhập tên người dùng"
                  />
                </div>
              )}
              
              <div>
                <label className="block text-sm font-medium mb-1 text-gray-700">Email</label>
                <input
                  type="email"
                  required
                  value={authForm.email}
                  onChange={(e) => setAuthForm({...authForm, email: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                  placeholder="Nhập email"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1 text-gray-700">
                  Mật khẩu (8-16 ký tự, phải có chữ HOA, thường, ký tự đặc biệt)
                </label>
                <input
                  type="password"
                  required
                  value={authForm.password}
                  onChange={(e) => setAuthForm({...authForm, password: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                  placeholder="Nhập mật khẩu (VD: Pass@123)"
                />
                {authForm.password && (
                  <div className="mt-2 space-y-1">
                    <p className={`text-xs ${authForm.password.length >= 8 && authForm.password.length <= 16 ? 'text-green-600' : 'text-red-600'}`}>
                      ✓ Độ dài: {authForm.password.length}/16 ký tự
                    </p>
                    <p className={`text-xs ${/[A-Z]/.test(authForm.password) ? 'text-green-600' : 'text-red-600'}`}>
                      {/[A-Z]/.test(authForm.password) ? '✓' : '✗'} Có chữ IN HOA
                    </p>
                    <p className={`text-xs ${/[a-z]/.test(authForm.password) ? 'text-green-600' : 'text-red-600'}`}>
                      {/[a-z]/.test(authForm.password) ? '✓' : '✗'} Có chữ thường
                    </p>
                    <p className={`text-xs ${/[!@#$%^&*(),.?":{}|<>]/.test(authForm.password) ? 'text-green-600' : 'text-red-600'}`}>
                      {/[!@#$%^&*(),.?":{}|<>]/.test(authForm.password) ? '✓' : '✗'} Có ký tự đặc biệt (!@#$%...)
                    </p>
                  </div>
                )}
              </div>
              
              {authError && (
                <div className="bg-red-50 text-red-600 px-4 py-2 rounded-lg text-sm">
                  {authError}
                </div>
              )}
              
              <button
                onClick={handleAuth}
                className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
              >
                {authMode === 'login' ? 'Đăng Nhập' : 'Đăng Ký'}
              </button>
            </div>
            
            <p className="text-center mt-4 text-sm text-gray-600">
              {authMode === 'login' ? 'Chưa có tài khoản? ' : 'Đã có tài khoản? '}
              <button
                onClick={() => {
                  setAuthMode(authMode === 'login' ? 'register' : 'login');
                  setAuthError('');
                }}
                className="text-blue-600 font-semibold hover:underline"
              >
                {authMode === 'login' ? 'Đăng ký ngay' : 'Đăng nhập'}
              </button>
            </p>
          </div>
          </div>
        )}

        {currentPage === 'home' && (
          <div className="container mx-auto">
            {/* Search and Filters */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="relative md:col-span-2">
                  <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="Tìm kiếm quạt..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                  />
                </div>
                
                <select
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                >
                  <option value="">Tất cả hãng</option>
                  {brands.map(brand => (
                    <option key={brand} value={brand}>{brand}</option>
                  ))}
                </select>
                
                <div className="flex gap-2">
                  <input
                    type="number"
                    placeholder="Giá từ"
                    value={priceRange.min || ''}
                    onChange={(e) => setPriceRange({...priceRange, min: Number(e.target.value) || 0})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                  />
                  <input
                    type="number"
                    placeholder="Giá đến"
                    value={priceRange.max === 10000000 ? '' : priceRange.max}
                    onChange={(e) => setPriceRange({...priceRange, max: Number(e.target.value) || 10000000})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-white text-gray-900"
                  />
                </div>
              </div>
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map(product => (
                <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="font-bold text-lg mb-2 text-gray-800">{product.name}</h3>
                    <p className="text-gray-600 text-sm mb-2">{product.description}</p>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-xs bg-blue-100 text-blue-600 px-2 py-1 rounded">
                        {product.brand}
                      </span>
                      <span className="text-lg font-bold text-blue-600">
                        {product.price.toLocaleString('vi-VN')}đ
                      </span>
                    </div>
                    <button
                      onClick={() => handleAddToCart(product.id)}
                      className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition flex items-center justify-center gap-2"
                    >
                      <ShoppingCart size={18} />
                      Thêm vào giỏ
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {products.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                Không tìm thấy sản phẩm nào!
              </div>
            )}
          </div>
        )}

        {currentPage === 'cart' && currentUser && (
          <div className="max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Giỏ Hàng Của Bạn</h2>
            
            {cart.length === 0 ? (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <ShoppingCart size={64} className="mx-auto text-gray-300 mb-4" />
                <p className="text-gray-500 mb-4">Giỏ hàng của bạn đang trống</p>
                <button
                  onClick={() => setCurrentPage('home')}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
                >
                  Tiếp tục mua sắm
                </button>
              </div>
            ) : (
              <>
                <div className="bg-white rounded-lg shadow-md mb-6">
                  {cart.map(item => {
                    const product = products.find(p => p.id === item.productId);
                    if (!product) return null;
                    
                    return (
                      <div key={item.productId} className="flex items-center gap-4 p-4 border-b last:border-b-0">
                        <img
                          src={product.image}
                          alt={product.name}
                          className="w-20 h-20 object-cover rounded"
                        />
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-800">{product.name}</h3>
                          <p className="text-sm text-gray-600">{product.brand}</p>
                          <p className="text-blue-600 font-bold">
                            {product.price.toLocaleString('vi-VN')}đ
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => handleUpdateCart(item.productId, item.quantity - 1)}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            <Minus size={18} />
                          </button>
                          <span className="w-8 text-center font-semibold">{item.quantity}</span>
                          <button
                            onClick={() => handleUpdateCart(item.productId, item.quantity + 1)}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            <Plus size={18} />
                          </button>
                        </div>
                        <button
                          onClick={() => handleRemoveFromCart(item.productId)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 size={20} />
                        </button>
                      </div>
                    );
                  })}
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xl font-semibold text-gray-800">Tổng cộng:</span>
                    <span className="text-2xl font-bold text-blue-600">
                      {getCartTotal().toLocaleString('vi-VN')}đ
                    </span>
                  </div>
                  <button className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition">
                    Thanh Toán
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;