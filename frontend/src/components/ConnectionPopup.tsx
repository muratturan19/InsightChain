import React, { useState } from 'react';

interface Props {
  onRetry: () => Promise<boolean>;
  onClose: () => void;
}

export default function ConnectionPopup({ onRetry, onClose }: Props) {
  const [showHelp, setShowHelp] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleRetry = async () => {
    const ok = await onRetry();
    if (ok) {
      setSuccess(true);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg max-w-md text-slate-900 dark:text-white space-y-4">
        {!success && (
          <>
            <p>
              İNTERNET BAĞLANTISI KURULAMADI.<br />
              Lütfen bağlantınızı kontrol edin ve 443 portuna erişimin açık olduğuna emin olun.
            </p>
            {showHelp && (
              <div className="text-sm space-y-2">
                <p>
                  İnternetinizin aktif olup olmadığını kontrol edin.<br />
                  • Tarayıcınızdan herhangi bir web sitesine (\u00f6rn. google.com, cnn.com) erişebiliyor musunuz?
                </p>
                <p>
                  Güvenlik Duvarı, Proxy veya VPN engeline takılmış olabilirsiniz.<br />
                  • Kurumsal ağdaysanız, IT departmanınıza danışın.<br />
                  • VPN, Proxy veya Antivirüs programları 443 portunu engelliyor olabilir.
                </p>
                <p>
                  443 portuna erişiminiz var mı?<br />
                  • 443 portu genellikle “güvenli (https)” bağlantılar için gereklidir.<br />
                  • Ağınızda ekstra bir firewall/antivirüs yazılımı varsa, bu portu engellemediğinden emin olun.
                </p>
                <p>
                  Yine de sorun devam ederse:<br />
                  • Bilgisayarınızı ve modem/router'ınızı yeniden başlatın.<br />
                  • Farklı bir ağdan (mobil hotspot, başka Wi-Fi) tekrar deneyin.<br />
                  • Detaylı destek için IT desteğiyle iletişime geçin.
                </p>
                <p>Gerekirse sistem yöneticinizle iletişime geçin.</p>
              </div>
            )}
            <div className="flex justify-between items-center pt-2">
              <button onClick={() => setShowHelp((v) => !v)} className="text-blue-700 underline text-sm">
                Yardım
              </button>
              <button onClick={handleRetry} className="px-3 py-1 bg-blue-900 text-white rounded">
                Tekrar Dene
              </button>
            </div>
          </>
        )}
        {success && (
          <div className="space-y-4">
            <p>✅ Bağlantı başarılı. Pencereyi kapatıp işlemlerinize devam edebilirsiniz.</p>
            <div className="flex justify-end">
              <button onClick={onClose} className="px-3 py-1 bg-blue-900 text-white rounded">
                Kapat
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
