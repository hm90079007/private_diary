from django .contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Diary

# 各テストメソッド実行前にログイン処理を行う
class LoggedInTestCase(TestCase):

    def setUp(self):
        self.password = 'test5100test'
        self.test_user = get_user_model().objects.create_user(username='testcase',email='testcase@testcase.com',password=self.password)
        self.client.login(email=self.test_user.email,password=self.password)

class TestDiaryCreateView(LoggedInTestCase):

    def test_create_diary_success(self):

        # 日記作成のための設定
        params = {'title':'testtitle','content':'this is test.',"photo1":"","photo2":"","photo3":""}
        response = self.client.post(reverse_lazy('diary:diary_create'),params)

        # 日記一覧ページに移動してから↑のリクエストを実行する。
        self.assertRedirects(response,reverse_lazy('diary:diary_list'))

        # DB検証して確認する。狙ったタイトルの数が1ならTrueを返答
        self.assertEqual(Diary.objects.filter(title='testtitle').count(),1)

    def test_create_diary_failure(self):

        response = self.client.post(reverse_lazy('diary:diary_create'))
        self.assertFormError(response,'form','title','This field is required.')

class TestDiaryUpdateView(LoggedInTestCase):

    def test_update_diary_success(self):

        diary = Diary.objects.create(user=self.test_user,title='before')
        params = {'title':'after'}
        response = self.client.post(reverse_lazy('diary:diary_update',kwargs={'pk':diary.pk}),params)
        self.assertRedirects(response,reverse_lazy('diary:diary_detail',kwargs={'pk':diary.pk}))
        self.assertEqual(Diary.objects.get(pk=diary.pk).title,'after')

    def test_update_dairy_failure(self):

        response = self.client.post(reverse_lazy('diary:diary_update',kwargs={'pk':999}))
        self.assertEqual(response.status_code,404)

class TestDiaryDeleteView(LoggedInTestCase):

    def test_delete_diary_success(self):

        diary = Diary.objects.create(user=self.test_user,title='before')
        response = self.client.post(reverse_lazy('diary:diary_delete',kwargs={'pk':diary.pk}))
        self.assertRedirects(response,reverse_lazy('diary:diary_list'))
        self.assertEqual(Diary.objects.filter(pk=diary.pk).count(),0)

    def test_delete_dairy_failure(self):

        response = self.client.post(reverse_lazy('diary:diary_update',kwargs={'pk':999}))
        self.assertEqual(response.status_code,404)
