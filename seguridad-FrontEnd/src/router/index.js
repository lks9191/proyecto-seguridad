// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue')
    },
    {
      path: '/2fa',
      name: 'two-factor',
      component: () => import('../views/auth/TwoFactorView.vue')
    },
    // --- RUTAS PROTEGIDAS (Requieren Autenticación y un Rol específico) ---
    {
      path: '/dashboard/user',
      name: 'user-dashboard',
      component: () => import('../views/dashboard/UserDashboard.vue'),
      meta: { requiresAuth: true, roles: ['USER', 'ADMIN'] } 
    },
    {
      path: '/dashboard/admin',
      name: 'admin-dashboard',
      component: () => import('../views/dashboard/AdminDashboard.vue'),
      meta: { requiresAuth: true, roles: ['ADMIN'] }
    },
    {
      path: '/dashboard/auditor',
      name: 'auditor-dashboard',
      component: () => import('../views/dashboard/AuditorDashboard.vue'),
      meta: { requiresAuth: true, roles: ['AUDITOR'] }
    },
    // --- RUTA DE ERROR ---
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/errors/UnauthorizedView.vue')
    }
  ]
})

// Guardia de Navegación Global
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 1. ¿La ruta requiere autenticación?
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Si no está autenticado, lo mandamos al login
    return next({ name: 'login' })
  }

  // 2. ¿La ruta requiere un rol específico? (Autorización / RBAC)
  if (to.meta.roles && authStore.isAuthenticated) {
    const userRole = authStore.role
    
    // Si el rol del usuario no está en la lista de roles permitidos para esta ruta
    if (!to.meta.roles.includes(userRole)) {
      return next({ name: 'unauthorized' }) // Principio de mínimo privilegio aplicado
    }
  }

  // 3. Si pasa todas las validaciones, permitimos el acceso
  next()
})

export default router