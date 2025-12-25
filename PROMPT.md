Мне нужно сделать веб приложение для составления расписания для дежурных врачей
Роли: врач, админ, сисадмин
Админ может: добавлять нового врача, менять врачей местами в расписании, просматривать статистику кто сколько дежурил часов в этом месяце, задавать время с __ по__ на все дни или на конкретный день (по умолчанию, дежурства в будни с 16:00 до 9:00 следующего дня, выходные с 9:00 до 9:00 следующего дня, но бывают праздники, в которые даже в будние дни дежурства могут быть сутки, плюс могут быть дни, когда дежуранты могут выходить по почереди, например один выходит с 9:00 до 17:00, а следующий с 17:00 до 9:00 следующего дня). Дни, когда выходят несколько дежурантов бывают редко, только если этот день очень сложно взять какому-то одному врачу, поэтому администратор согласует с каждым врачом индивидуально и сам ставит на этот день врачей с... по ... Также, админ может устанавливать каждому врачу минимальное количество дежурств в месяц и приоритет (для автоматического составления см. ниже)
Врач может писать дни, когда ему удобно выйти в каком-то месяце, например, в ноябре удобно: 3, 5, 7, 20 (на фронтенде будет выбирать из календаря). Просматривать расписания дежурств, в том числе, которое еще не до конца заполнено, но если Админ нажмет на visible=true. Меняться дежурствами с другими врачами или отменять дежурство, но сама отмена или замена происходит только после того, как Админ это одобрит. Просматривать статистику, сколько он дежурил и в каком месяце, просматривать историю расписаний. 
Сисадмин может назначать администраторов, добавлять врачей. Сисадмин может также быть врачом. То есть, у него права те же, что и у админа и врача, плюс он может назначать и переназначать роли и видеть всех врачей и администраторов.
Принцип работы:
Админ (или сисадмин) логинится и добавляет email и telegram username врачей
Врач логинится, видит график дежурств на текущий месяц, в боковом меню функционал для установки удобных дней на следующий месяц. При установке можно нажать на скопировать из прошлого месяца. После нажать на Отправить и эти дни отправляются администратору.
Администратор видит график на текущий месяц и также рядом с ним график на следующий месяц. Когда приходят удобные дни дежурств на следующий месяц, админ видит их на графике. Если несколько врачей ставят один и тот же день, админ видит, что в этот день хотят несколько врачей. Админ может нажать на "Сформировать автоматически" и тогда график составляется комбинаторикой с учетом: 1. пожеланий врача, 2. минимального количества дежурств для врача, 3. чем выше приоритет, тем вероятнее данный врач будет ставиться на день, в который хотят выйти несколько врачей, 4. Нельзя, чтобы автоматически формировалось так, чтобы один врач дежурил 2 дня подряд, это может делать только админ вручную. Администратор может несколько раз нажимать на сформировать автоматически, чтобы перебирать варианты. После того, как черновой вариант его устроит, он может ставить врачей вручную путем перетаскивания. Список врачей он видит в виде небольших карточек... наверное лучше под самим графиком. Он может оттуда делать drag and drop врача в расписание. В самом расписании и в пустых клетках и когда там врач должно быть указано: день недели, дата и с какого часа дежурство, например: 28, Вс, 9:00 (или придумай, как сделать, чтобы было понятно, что в этот день дежурство с 9 или 16 часов). Если в один день дежурят несколько врачей, то при перетаскивании второго врача, откроется меню, где можно устанавливать время для каждого врача.
После того, как расписание полностью сформировано, админ нажимает на Опубликовать и расписание видят все врачи.
Также админ в навбаре может нажать на статистика, там будет что-то вроде дашборда, под которым будет список всех врачей и рядом с каждым данные по его приоритету, мин количеством дней дежурств (или лучше часов но это как-то нужно адаптировать для автоматического формирования графика), сколько дежурств (и часов) взял

Архитектура:
Бекенд на fastapi, sqlmodels. Каждая абстракция в отдельном модуле, например, модуль польозвателей: ./app/modules/users в нем: models.py, schemas.py, enums.py (если нужно), utils.py (тут служебные функции для данного модуля), routers.py. Потом все routers импортируются в main.py. В ./app/core служеюные файлы: config.py, db.py, security.py. В ./app/.env переменные, которые затем импортируются в config.py . Пока пусть при добавлении пользователя, пароль просто генерится, а сам пользователь его потом меняет на собственный в приложении. Если пользователь забыл пароль, администратор генерит еще один и отправляет пользователю. Пока так. не будем с почтой заморачиваться. Еще, чтобы не было проблем с Relationship полями, посмотри, как это было сделано в другом моем проекте:
# ./app/modules/users/models.py

from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UserAvatar(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    file_path: str
    is_primary: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: "User" = Relationship(back_populates="avatars")

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    hashed_password: Optional[str] = None
    nickname: Optional[str] = None
    is_admin: bool = False
    is_author: bool = False
    is_active: bool = True
    is_verified: bool = False
    is_blocked: bool = False
    coins_balance: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

    is_adult: bool = Field(default=False)
    preferred_gender: Optional[str] = Field(default=None, index=True)
    
    # 👇 Настройка приватности: размытие лица на фото
    blur_face: bool = Field(default=True)

    avatars: List[UserAvatar] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    characters: List["Character"] = Relationship(back_populates="owner")
    likes: List["CharacterLike"] = Relationship(back_populates="user")
    chats: List["Chat"] = Relationship(back_populates="user")
    transactions: List["CoinTransaction"] = Relationship(back_populates="user")

UserAvatar.user = Relationship(back_populates="avatars", sa_relationship_kwargs={"lazy":"joined"})

Фронтенд на nuxt4, pinia store (только на .js composition api), tailwinds, daisyui
Пример store:
// frontend/app/stores/user.js

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const items = ref([])
  const q = ref('')
  const loading = ref(false)
  const limit = ref(5)
  const offset = ref(0)

  function reset() {
    user.value = null
  }

  async function fetchMe() {
    const { $api } = useNuxtApp()
    user.value = await $api('/users/me')
    return user.value
  }

  async function updateMe(payload) {
    const { $api } = useNuxtApp()
    user.value = await $api('/users/me', { method: 'PATCH', body: payload })
    return user.value
  }

  async function updateNickname(nickname) {
    return updateMe({ nickname })
  }

  async function updatePreferredGender(preferred_gender) {
    return updateMe({ preferred_gender })
  }

  // ==========================================
  // Security / Privacy settings
  // ==========================================
  
  async function updateBlurFace(blur_face) {
    return updateMe({ blur_face })
  }

  async function getSecuritySettings() {
    const { $api } = useNuxtApp()
    return await $api('/security/settings')
  }

  async function updateSecuritySettings(payload) {
    const { $api } = useNuxtApp()
    const result = await $api('/security/settings', { method: 'PATCH', body: payload })
    // Синхронизируем с user если нужно
    if (user.value && payload.blur_face !== undefined) {
      user.value.blur_face = payload.blur_face
    }
    return result
  }

  // Превью размытия (для тестирования)
  async function testBlurPreview(file) {
    const { $api } = useNuxtApp()
    const fd = new FormData()
    fd.append('file', file)
    return await $api('/security/blur-preview', { 
      method: 'POST', 
      body: fd, 
      headers: {} 
    })
  }

  // ==========================================
  // Avatar methods
  // ==========================================

  async function uploadAvatar(file) {
    const { $api } = useNuxtApp()
    const fd = new FormData()
    fd.append('file', file)
    const res = await $api('/users/me/avatar', { method: 'POST', body: fd, headers: {} })
    await fetchMe()
    return res
  }

  async function setPrimaryAvatar(avatarId) {
    const { $api } = useNuxtApp()
    await $api(`/users/me/avatar/${avatarId}/primary`, { method: 'POST' })
    await fetchMe()
  }

  async function deleteAvatar(avatarId) {
    const { $api } = useNuxtApp()
    await $api(`/users/me/avatar/${avatarId}`, { method: 'DELETE' })
    await fetchMe()
  }

  // ==========================================
  // Password & Email
  // ==========================================

  async function changePassword(old_password, new_password) {
    const { $api } = useNuxtApp()
    await $api('/users/me/password/change', { method: 'POST', body: { old_password, new_password } })
  }

  async function requestEmailChange(new_email) {
    const { $api } = useNuxtApp()
    await $api('/users/me/email/change/request', { method: 'POST', body: { new_email } })
  }

  // ==========================================
  // Admin methods
  // ==========================================

  async function fetchUsers() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const qs = new URLSearchParams()
      if (q.value) qs.set('q', q.value)
      qs.set('limit', String(limit.value))
      qs.set('offset', String(offset.value))
      const res = await $api(`/users/?${qs.toString()}`)
      items.value = res || []
    } finally {
      loading.value = false
    }
  }

  async function adminUpdateUser(userId, payload) {
    const { $api } = useNuxtApp()
    const updated = await $api(`/users/${userId}`, { method: 'PATCH', body: payload })
    const idx = (items.value || []).findIndex(x => x.id === userId)
    if (idx !== -1) items.value[idx] = updated
    return updated
  }

  // ==========================================
  // Computed helpers
  // ==========================================
  
  const isBlurFaceEnabled = computed(() => user.value?.blur_face ?? true)
  const primaryAvatarUrl = computed(() => user.value?.primary_avatar_url)
  const hasAvatars = computed(() => (user.value?.avatars?.length ?? 0) > 0)

  return {
    // State
    user,
    items,
    q,
    limit,
    offset,
    loading,

    // Computed
    isBlurFaceEnabled,
    primaryAvatarUrl,
    hasAvatars,

    // Actions
    reset,
    fetchMe,
    updateMe,
    updateNickname,
    updatePreferredGender,
    
    // Security
    updateBlurFace,
    getSecuritySettings,
    updateSecuritySettings,
    testBlurPreview,

    // Avatars
    uploadAvatar,
    setPrimaryAvatar,
    deleteAvatar,

    // Password & Email
    changePassword,
    requestEmailChange,

    // Admin
    fetchUsers,
    adminUpdateUser,
  }
})

Все должно делиться на компоненты, layouts (для админа и врача и для мобильных устройств при необходимости), utils, composables, plugins, middleware
Каждый .vue файл должен быть в таком виде:
сначала <script setup></script>
затем <template></template>
и в самом конце <style scoped></style> если нужно

В начале каждого файла и на фронтенде и на бекенде нужно в комментариях писать его relative path, например: // frontend/app/stores/user.js , <!-- ./pages/admin/users/index.vue -->, # ./app/modules/users/models.py

в nuxt4 компонент ./app/components/Ui/Navbar.vue в других компонентах или на странице или на layout будет выглядеть так: <UiNavbar/>